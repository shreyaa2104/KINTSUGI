from utils.dataset_context import get_dataset_context
from utils.planner import create_plan
from utils.tool_executor import execute_tool
from utils.schemas import Intent
from utils.ai_insights import generate_ai_insights


def run_agent(df, user_query, chat_memory=None, ai_memory=None):
    """
    Runs the KINTSUGI AI agent.
    """

    dataset_context = get_dataset_context(df)

    memory_context = ""

    if chat_memory:
        memory_context = "\n\nPrevious Conversation:\n"

        for chat in chat_memory[-5:]:
            memory_context += (
                f"User: {chat['user']}\n"
                f"Assistant: {chat['assistant']}\n\n"
            )

    plan = create_plan(
        question=user_query,
        dataset_context=dataset_context,
        chat_memory=chat_memory,
        ai_memory=None
    )

    print("=" * 60)

    for i, step in enumerate(plan.steps, start=1):
        print(f"Step {i}")
        print("Intent:", step.intent)
        print("Parameters:", step.parameters)
        print("-" * 40)

    print("=" * 60)

    responses = []

    current_df = df

    for step in plan.steps:

        if step.intent == Intent.AI_ANALYSIS:

            insights = generate_ai_insights(current_df)

            responses.append({
                "type": "analysis",
                "response": insights
            })

            continue

        try:
            result = execute_tool(current_df, step)

        except Exception as e:

            responses.append({
                "type": "error",
                "message": str(e)
            })

            break

        responses.append(result)

        # Update AI working memory
        if ai_memory is not None:

            ai_memory = {
                "last_operation": step.intent.value,
                "last_message": result["message"],
                "last_columns": [],
                "last_chart": None
            }

            if "column" in step.parameters:
                ai_memory["last_columns"] = [step.parameters["column"]]

            elif "columns" in step.parameters:
                ai_memory["last_columns"] = step.parameters["columns"]

        if result["type"] == "dataframe":

            current_df = result["data"]

            if result["message"].startswith("❌"):
                break

    return {
        "type": "multi_step",
        "responses": responses,
        "final_df": current_df,
        "plan": plan
    }