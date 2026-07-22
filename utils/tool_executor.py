from utils.schemas import Intent

# Cleaning
from utils.cleaning import (
    remove_duplicates,
    replace_null_values,
    sort_dataframe,
)

# Editing
from utils.editing import (
    rename_column,
    delete_column,
    filter_dataframe,
    replace_values,
    update_cell_value,
    create_new_column,
)

# Visualization
from utils.vizualization import create_visualization


TOOL_MAP = {
    Intent.REMOVE_DUPLICATES: remove_duplicates,
    Intent.REPLACE_NULL_VALUES: replace_null_values,
    Intent.SORT_DATA: sort_dataframe,

    Intent.RENAME_COLUMN: rename_column,
    Intent.DELETE_COLUMN: delete_column,
    Intent.FILTER_DATA: filter_dataframe,
    Intent.REPLACE_VALUES: replace_values,
    Intent.UPDATE_CELL: update_cell_value,
    Intent.CREATE_NEW_COLUMN: create_new_column,

    Intent.CREATE_VISUALIZATION: create_visualization,
}


def execute_tool(df, plan):
    """
    Execute the tool selected by the planner.
    """

    tool = TOOL_MAP.get(plan.intent)

    if tool is None:
        raise ValueError(f"Unsupported intent: {plan.intent}")

    if plan.intent == Intent.CREATE_VISUALIZATION:

        fig, message = tool(df, **plan.parameters)

        return {
            "type": "visualization",
            "figure": fig,
            "message": message
        }

    updated_df, message = tool(df, **plan.parameters)

    return {
        "type": "dataframe",
        "data": updated_df,
        "message": message
    }