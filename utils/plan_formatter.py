from utils.schemas import AgentPlan
INTENT_NAMES = {
    "AI_ANALYSIS": "Analyze Dataset",
    "REMOVE_DUPLICATES": "Remove Duplicate Rows",
    "REPLACE_NULL_VALUES": "Replace Missing Values",
    "SORT_DATA": "Sort Dataset",
    "RENAME_COLUMN": "Rename Column",
    "DELETE_COLUMN": "Delete Column",
    "FILTER_DATA": "Filter Rows",
    "REPLACE_VALUES": "Replace Values",
    "UPDATE_CELL": "Update Cell",
    "CREATE_NEW_COLUMN": "Create New Column",
    "CREATE_VISUALIZATION": "Create Visualization",
    "DOWNLOAD_DATASET": "Download Dataset",
}


def format_execution_plan(plan: AgentPlan) -> str:
    """Convert an AgentPlan into a readable execution plan."""

    lines = ["## 📝 Execution Plan\n"]

    for index, step in enumerate(plan.steps, start=1):
        lines.append(f"### Step {index}")
        friendly_name = INTENT_NAMES.get(step.intent.value, step.intent.value)

        lines.append(f"🔧 **{friendly_name}**")

        if step.parameters:
            lines.append("**Parameters:**")

            for key, value in step.parameters.items():
                pretty_key = key.replace("_", " ").title()
                lines.append(f"- **{pretty_key}:** {value}")

        else:
            lines.append("No parameters")

        lines.append("")

    return "\n".join(lines)