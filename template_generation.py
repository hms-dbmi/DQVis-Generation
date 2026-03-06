import pandas as pd
from udi_grammar_py import Chart, Op, rolling
from enum import Enum

class QueryType(Enum):
    QUESTION = "question"
    UTTERANCE = "utterance"

class ChartType(Enum):
    SCATTERPLOT = "scatterplot"
    BARCHART = "barchart"
    GROUPED_BAR = "stacked_bar"
    STACKED_BAR = "stacked_bar"
    NORMALIZED_BAR = "stacked_bar"
    CIRCULAR = "circular"
    TABLE = "table"
    LINE = "line"
    AREA = "area"
    GROUPED_LINE = "grouped_line"
    GROUPED_AREA = "grouped_area"
    GROUPED_SCATTER = "grouped_scatter"
    HEATMAP = "heatmap"
    HISTOGRAM = "histogram"
    DOT = "dot"
    GROUPED_DOT = "grouped_dot"

class TaskType(Enum):
    RETRIEVE_VALUE = "Retrieve_Value"
    FILTER = "Filter"
    COMPUTE_DERIVED_VALUE = "Compute_Derived_Value"
    FIND_EXTREMUM = "Find_Extremum"
    SORT = "Sort"
    DETERMINE_RANGE = "Determine_Range"
    CHARACTERIZE_DISTRIBUTION = "Characterize_Distribution"
    FIND_ANOMALIES = "Find_Anomalies"
    CLUSTER = "Cluster"
    CORRELATE = "Correlate"


def add_row(df, query_template, spec, constraints, query_type: QueryType, chart_type: ChartType, task_types: list[TaskType], description: str = "", design_considerations: str = "", tasks: str = ""):
    spec_key_count = get_total_key_count(spec.to_dict())
    if spec_key_count <= 12:
        complexity = "simple"
    elif spec_key_count <= 24:
        complexity = "medium"
    elif spec_key_count <= 36:
        complexity = "complex"
    else:
        complexity = "extra complex"
    df.loc[len(df)] = {
        "query_template": query_template,
        "constraints": constraints,
        "spec_template": spec.to_json(),
        "query_type": query_type.value,
        "creation_method": "template",
        "chart_type": chart_type.value,
        "chart_complexity": complexity,
        "spec_key_count": spec_key_count,
        "task_types": task_types,
        "description": description,
        "design_considerations": design_considerations,
        "tasks": tasks
    }
    return df

def get_total_key_count(nested_dict):
    if isinstance(nested_dict, dict):
        return sum(get_total_key_count(value) for value in nested_dict.values())
    elif isinstance(nested_dict, list):
        return sum(get_total_key_count(item) for item in nested_dict)
    else:
        return 1

def generate():
    df = pd.DataFrame(
        columns=[
            "query_template",
            "constraints",
            "spec_template",
            "query_type",
            "creation_method",
            "chart_type",
            "chart_complexity",
            "spec_key_count",
            "task_types",
            "description",
            "design_considerations",
            "tasks"
        ]
    )

    # Define recurring constraints
    overlap = "F1['name'] in F2['udi:overlapping_fields'] or F2['udi:overlapping_fields'] == 'all'"


    df = add_row(
        df,
        query_template="How many <E> are there, grouped by <F:n>?",
        spec=(
            Chart()
            .source("<E>", "<E.url>")
            .groupby("<F>")
            .rollup({"<E> count": Op.count()})
            .mark("bar")
            .x(field="<F>", type="nominal")
            .y(field="<E> count", type="quantitative")
        ),
        constraints=[
            "F.c * 2 < E.c",
            "F.c <= 4",
            "F.c > 1",
        ],
        query_type=QueryType.QUESTION,
        chart_type=ChartType.BARCHART,
        task_types=[
            TaskType.COMPUTE_DERIVED_VALUE,
        ],
        description="Counts entities grouped by a nominal field, displayed as a vertical bar chart.",
        design_considerations="Vertical orientation chosen because category count is small (<=4), keeping x-axis labels readable.",
        tasks="Compare counts across categories; identify the most or least common category.",

    )

    df = add_row(
        df,
        query_template="How many <E> are there, grouped by <F:n>?",
        spec=(
            Chart()
            .source("<E>", "<E.url>")
            .groupby("<F>")
            .rollup({"<E> count": Op.count()})
            .mark("bar")
            .x(field="<E> count", type="quantitative")
            .y(field="<F>", type="nominal")
        ),
        constraints=[
            "F.c * 2 < E.c",
            "F.c > 4",
            "F.c < 25",
        ],
        query_type=QueryType.QUESTION,
        chart_type=ChartType.BARCHART,
        task_types=[
            TaskType.COMPUTE_DERIVED_VALUE,
        ],
        description="Counts entities grouped by a nominal field, displayed as a horizontal bar chart.",
        design_considerations="Horizontal orientation chosen because category count is high (>4), allowing longer labels on the y-axis.",
        tasks="Compare counts across categories; identify the most or least common category.",

    )


    df = add_row(
        df,
        query_template="Make a bar chart of <E> <F:n>.",
        spec=(
            Chart()
            .source("<E>", "<E.url>")
            .groupby("<F>")
            .rollup({"<E> count": Op.count()})
            .mark("bar")
            .x(field="<F>", type="nominal")
            .y(field="<E> count", type="quantitative")
        ),
        constraints=[
            "F.c * 2 < E.c",
            "F.c <= 4",
            "F.c > 1",
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.BARCHART,
        task_types=[
            TaskType.COMPUTE_DERIVED_VALUE,
            TaskType.DETERMINE_RANGE
        ],
        description="Creates a vertical bar chart counting entities by a nominal field.",
        design_considerations="Vertical orientation for small category counts (<=4). Count aggregation applied automatically.",
        tasks="Compare counts across categories; identify the most or least common category; assess the range of counts.",

    )

    df = add_row(
        df,
        query_template="Make a bar chart of <E> <F:n>.",
        spec=(
            Chart()
            .source("<E>", "<E.url>")
            .groupby("<F>")
            .rollup({"<E> count": Op.count()})
            .mark("bar")
            .x(field="<E> count", type="quantitative")
            .y(field="<F>", type="nominal")
        ),
        constraints=[
            "F.c * 2 < E.c",
            "F.c > 4",
            "F.c < 25",
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.BARCHART,
        task_types=[
            TaskType.COMPUTE_DERIVED_VALUE,
            TaskType.DETERMINE_RANGE
        ],
        description="Creates a horizontal bar chart counting entities by a nominal field.",
        design_considerations="Horizontal orientation for higher category counts (>4), improving label readability.",
        tasks="Compare counts across categories; identify the most or least common category; assess the range of counts.",

    )

    df = add_row(
        df,
        query_template="How many <E1> are there, grouped by <E2.F:n>?",
        spec=(
            Chart()
            .source("<E1>", "<E1.url>")
            .source("<E2>", "<E2.url>")
            .join(
                in_name=['<E1>', '<E2>'],
                on=['<E1.r.E2.id.from>', '<E1.r.E2.id.to>'],
                out_name='<E1>__<E2>',
            )
            .groupby("<E2.F>")
            .rollup({"<E1> count": Op.count()})
            .mark("bar")
            .x(field="<E2.F>", type="nominal")
            .y(field="<E1> count", type="quantitative")
        ),
        constraints=[
            "E2.F.c * 2 < E1.c",
            "E2.F.c <= 4",
            "E2.F.c > 1",
            "E1.r.E2.c.to == 'one'",
            "E2.F.name not in E1.fields"
        ],
        query_type=QueryType.QUESTION,
        chart_type=ChartType.BARCHART,
        task_types=[
            TaskType.COMPUTE_DERIVED_VALUE,
        ],
        description="Joins two entities and counts records grouped by a field from the related entity, displayed as a vertical bar chart.",
        design_considerations="Cross-entity join groups by a field not native to the counted entity. Vertical orientation for small category counts (<=4). Requires a many-to-one relationship.",
        tasks="Compare counts across categories from a related entity; discover cross-entity frequency patterns.",

    )

    df = add_row(
        df,
        query_template="How many <E1> are there, grouped by <E2.F:n>?",
        spec=(
            Chart()
            .source("<E1>", "<E1.url>")
            .source("<E2>", "<E2.url>")
            .join(
                in_name=['<E1>', '<E2>'],
                on=['<E1.r.E2.id.from>', '<E1.r.E2.id.to>'],
                out_name='<E1>__<E2>',
            )
            .groupby("<E2.F>")
            .rollup({"<E1> count": Op.count()})
            .mark("bar")
            .x(field="<E1> count", type="quantitative")
            .y(field="<E2.F>", type="nominal")
        ),
        constraints=[
            "E2.F.c * 2 < E1.c",
            "E2.F.c > 4",
            "E2.F.c < 25",
            "E1.r.E2.c.to == 'one'",
            "E2.F.name not in E1.fields"
        ],
        query_type=QueryType.QUESTION,
        chart_type=ChartType.BARCHART,
        task_types=[
            TaskType.COMPUTE_DERIVED_VALUE,
        ],
        description="Joins two entities and counts records grouped by a field from the related entity, displayed as a horizontal bar chart.",
        design_considerations="Cross-entity join with horizontal orientation for higher category counts (>4). Requires a many-to-one relationship.",
        tasks="Compare counts across categories from a related entity; discover cross-entity frequency patterns.",

    )

    df = add_row(
        df,
        query_template=f"How many <E1> are there, grouped by <E1.F1:n> and <E2.F2:n>?",
        spec=(
            Chart()
            .source("<E1>", "<E1.url>")
            .source("<E2>", "<E2.url>")
            .join(
                in_name=['<E1>', '<E2>'],
                on=['<E1.r.E2.id.from>', '<E1.r.E2.id.to>'],
                out_name='<E1>__<E2>',
            )
            .groupby(["<E2.F2>", "<E1.F1>"])
            .rollup({"count <E1>": Op.count()})
            .mark("bar")
            .y(field="count <E1>", type="quantitative")
            .color(field="<E2.F2>", type="nominal")
            .x(field="<E1.F1>", type="nominal")
        ),
        constraints=[
            "E1.F1.c * 2 < E1.c",
            "E2.F2.c * 2 < E2.c",
            "E1.F1.c > 1",
            "E2.F2.c > 1",
            "E1.F1.c <= 4",
            "E2.F2.c <= 4",
            "E1.F1.c >= E2.F2.c",
            "E1.r.E2.c.to == 'one'",
            "E2.F2.name not in E1.fields",
            "E1.F1.name not in E2.fields",
        ],
        query_type=QueryType.QUESTION,
        chart_type=ChartType.STACKED_BAR,
        task_types=[
            TaskType.COMPUTE_DERIVED_VALUE,
        ],
        description="Joins two entities and produces a vertical stacked bar chart of counts grouped by two nominal fields.",
        design_considerations="Stacked bars show part-to-whole composition within each category. Vertical layout for small category counts (<=4). Color encodes the secondary grouping field from the related entity. Color is preferably mapped to the variable with fewer unique values for better discriminability.",
        tasks="Compare group compositions across categories; identify dominant sub-groups within each bar.",

    )

    df = add_row(
        df,
        query_template=f"How many <E1> are there, grouped by <E1.F1:n> and <E2.F2:n>?",
        spec=(
            Chart()
            .source("<E1>", "<E1.url>")
            .source("<E2>", "<E2.url>")
            .join(
                in_name=['<E1>', '<E2>'],
                on=['<E1.r.E2.id.from>', '<E1.r.E2.id.to>'],
                out_name='<E1>__<E2>',
            )
            .groupby(["<E2.F2>", "<E1.F1>"])
            .rollup({"count <E1>": Op.count()})
            .mark("bar")
            .x(field="count <E1>", type="quantitative")
            .color(field="<E1.F1>", type="nominal")
            .y(field="<E2.F2>", type="nominal")
        ),
        constraints=[
            "E1.F1.c * 2 < E1.c",
            "E2.F2.c * 2 < E2.c",
            "E1.F1.c > 1",
            "E1.F1.c < 25",
            "E2.F2.c > 1",
            "E2.F2.c < 25",
            "E1.F1.c > 4 or E2.F2.c > 4",
            "E1.F1.c <= E2.F2.c",
            "E1.r.E2.c.to == 'one'",
            "E2.F2.name not in E1.fields",
            "E1.F1.name not in E2.fields",
        ],
        query_type=QueryType.QUESTION,
        chart_type=ChartType.STACKED_BAR,
        task_types=[
            TaskType.COMPUTE_DERIVED_VALUE,
        ],
        description="Joins two entities and produces a horizontal stacked bar chart of counts grouped by two nominal fields.",
        design_considerations="Horizontal orientation for higher category counts (>4). Color encodes the primary grouping field. Cross-entity join required. Color is preferably mapped to the variable with fewer unique values for better discriminability.",
        tasks="Compare group compositions across categories; identify dominant sub-groups within each bar.",

    )

    df = add_row(
        df,
        query_template=f"How many <E> are there, grouped by <F1:n> and <F2:n>?",
        spec=(
            Chart()
            .source("<E>", "<E.url>")
            .groupby(["<F2>", "<F1>"])
            .rollup({"count <E>": Op.count()})
            .mark("bar")
            .y(field="count <E>", type="quantitative")
            .color(field="<F1>", type="nominal")
            .x(field="<F2>", type="nominal")
        ),
        constraints=[
            "F1.c * 2 < E.c",
            "F2.c * 2 < E.c",
            "F1.c > 1",
            "F2.c > 1",
            "F1.c <= 4",
            "F2.c <= 4",
            "F2.c >= F1.c",
            overlap,
        ],
        query_type=QueryType.QUESTION,
        chart_type=ChartType.STACKED_BAR,
        task_types=[
            TaskType.COMPUTE_DERIVED_VALUE,
        ],
        description="Counts entities grouped by two nominal fields, displayed as a vertical stacked bar chart.",
        design_considerations="Vertical stacked layout for small category counts (<=4). Color encodes the sub-group field; x-axis shows the primary grouping. Color is preferably mapped to the variable with fewer unique values for better discriminability.",
        tasks="Compare group compositions across categories; identify dominant sub-groups within each bar.",

    )

    df = add_row(
        df,
        query_template=f"How many <E> are there, grouped by <F1:n> and <F2:n>?",
        spec=(
            Chart()
            .source("<E>", "<E.url>")
            .groupby(["<F1>", "<F2>"])
            .rollup({"count <E>": Op.count()})
            .mark("bar")
            .x(field="count <E>", type="quantitative")
            .color(field="<F1>", type="nominal")
            .y(field="<F2>", type="nominal")
        ),
        constraints=[
            "F1.c * 2 < E.c",
            "F2.c * 2 < E.c",
            "F1.c > 4 or F2.c > 4",
            "F1.c > 1",
            "F1.c < 25",
            "F2.c > 1",
            "F2.c < 25",
            "F2.c >= F1.c",
            overlap,
        ],
        query_type=QueryType.QUESTION,
        chart_type=ChartType.STACKED_BAR,
        task_types=[
            TaskType.COMPUTE_DERIVED_VALUE,
        ],
        description="Counts entities grouped by two nominal fields, displayed as a horizontal stacked bar chart.",
        design_considerations="Horizontal stacked layout for higher category counts (>4). Color encodes the sub-group field. Color is preferably mapped to the variable with fewer unique values for better discriminability.",
        tasks="Compare group compositions across categories; identify dominant sub-groups within each bar.",

    )

    df = add_row(
        df,
        query_template=f"What is the count of <F1:n> for each <F2:n>?",
        spec=(
            Chart()
            .source("<E>", "<E.url>")
            .groupby(["<F1>", "<F2>"])
            .rollup({"count <E>": Op.count()})
            .mark("bar")
            .y(field="count <E>", type="quantitative")
            .xOffset(field="<F1>", type="nominal")
            .color(field="<F1>", type="nominal")
            .x(field="<F2>", type="nominal")
        ),
        constraints=[
            "F1.c * 2 < E.c",
            "F2.c * 2 < E.c",
            "F1.c > 1",
            "F2.c > 1",
            "F1.c <= 4",
            "F2.c <= 4",
            overlap,
        ],
        query_type=QueryType.QUESTION,
        chart_type=ChartType.GROUPED_BAR,
        task_types=[
            TaskType.COMPUTE_DERIVED_VALUE,
        ],
        description="Counts entities grouped by two nominal fields, displayed as a grouped (side-by-side) vertical bar chart.",
        design_considerations="Uses xOffset for side-by-side grouping, allowing direct comparison between sub-groups. Suitable for small category counts (<=4).",
        tasks="Directly compare sub-group counts within and across categories.",

    )

    df = add_row(
        df,
        query_template=f"What is the count of <F1:n> for each <F2:n>?",
        spec=(
            Chart()
            .source("<E>", "<E.url>")
            .groupby(["<F1>", "<F2>"])
            .rollup({"count <E>": Op.count()})
            .mark("bar")
            .x(field="count <E>", type="quantitative")
            .yOffset(field="<F1>", type="nominal")
            .color(field="<F1>", type="nominal")
            .y(field="<F2>", type="nominal")
        ),
        constraints=[
            "F1.c * 2 < E.c",
            "F2.c * 2 < E.c",
            "F1.c > 4 or F2.c > 4",
            "F1.c > 1",
            "F1.c < 5",
            "F2.c > 1",
            "F2.c < 25",
            "F2.c >= F1.c",
            overlap,
        ],
        query_type=QueryType.QUESTION,
        chart_type=ChartType.GROUPED_BAR,
        task_types=[
            TaskType.COMPUTE_DERIVED_VALUE,
        ],
        description="Counts entities grouped by two nominal fields, displayed as a grouped (side-by-side) horizontal bar chart.",
        design_considerations="Uses yOffset for side-by-side grouping in horizontal orientation. Chosen when at least one field has more than 4 categories.",
        tasks="Directly compare sub-group counts within and across categories.",

    )

    df = add_row(
        df,
        query_template=f"What is the count of <F1:n> for each <F2:n>?",
        spec=(
            Chart()
            .source("<E>", "<E.url>")
            .groupby(["<F1>", "<F2>"])
            .rollup({"count <E>": Op.count()})
            .mark("bar")
            .x(field="count <E>", type="quantitative")
            .color(field="<F1>", type="nominal")
            .y(field="<F2>", type="nominal")
        ),
        constraints=[
            "F1.c * 2 < E.c",
            "F2.c * 2 < E.c",
            "F1.c > 4 or F2.c > 4",
            "F1.c > 1",
            "F1.c < 10",
            "F2.c > 1",
            "F2.c < 25",
            "F2.c >= F1.c",
            overlap,
        ],
        query_type=QueryType.QUESTION,
        chart_type=ChartType.STACKED_BAR,
        task_types=[
            TaskType.COMPUTE_DERIVED_VALUE
        ],
        description="Counts entities grouped by two nominal fields, displayed as a horizontal stacked bar chart.",
        design_considerations="Horizontal stacked layout for higher category counts (>4). Color encodes the sub-group; stacking shows part-to-whole within each bar. Allows up to 10 sub-group categories. Color is preferably mapped to the variable with fewer unique values for better discriminability.",
        tasks="Compare group compositions across categories; identify dominant sub-groups within each bar.",

    )


    df = add_row(
        df,
        query_template=f"What is the frequency of <F1:n> for each <F2:n>?",
        spec=(
            Chart()
            .source("<E>", "<E.url>")
            .groupby("<F2>", out_name="groupCounts")
            .rollup({"<F2>_count": Op.count()})
            .groupby(["<F1>", "<F2>"], in_name="<E>")
            .rollup({"<F1>_and_<F2>_count": Op.count()})
            .join(
                in_name=["<E>", "groupCounts"],
                on="<F2>",
                out_name="datasets",
            )
            .derive({"frequency": "d['<F1>_and_<F2>_count'] / d['<F2>_count']"})
            .mark("bar")
            .y(field="frequency", type="quantitative")
            .color(field="<F1>", type="nominal")
            .x(field="<F2>", type="nominal")
        ),
        constraints=[
            "F1.c * 2 < E.c",
            "F2.c * 2 < E.c",
            "F1.c > 1",
            "F2.c > 1",
            "F1.c <= 4",
            "F2.c <= 4",
            overlap,
        ],
        query_type=QueryType.QUESTION,
        chart_type=ChartType.NORMALIZED_BAR,
        task_types=[
            TaskType.COMPUTE_DERIVED_VALUE
        ],
        description="Shows the frequency (proportion) of one nominal field within each category of another, as a vertical normalized bar chart.",
        design_considerations="Normalization computes proportions per group, enabling fair comparison across groups of different sizes. Vertical layout for small category counts (<=4). Color is preferably mapped to the variable with fewer unique values for better discriminability.",
        tasks="Compare relative proportions across categories; identify which sub-groups dominate in each group.",

    )

    df = add_row(
        df,
        query_template=f"What is the frequency of <F1:n> for each <F2:n>?",
        spec=(
            Chart()
            .source("<E>", "<E.url>")
            .groupby("<F2>", out_name="groupCounts")
            .rollup({"<F2>_count": Op.count()})
            .groupby(["<F1>", "<F2>"], in_name="<E>")
            .rollup({"<F1>_and_<F2>_count": Op.count()})
            .join(
                in_name=["<E>", "groupCounts"],
                on="<F2>",
                out_name="datasets",
            )
            .derive({"frequency": "d['<F1>_and_<F2>_count'] / d['<F2>_count']"})
            .mark("bar")
            .x(field="frequency", type="quantitative")
            .color(field="<F1>", type="nominal")
            .y(field="<F2>", type="nominal")
        ),
        constraints=[
            "F1.c * 2 < E.c",
            "F2.c * 2 < E.c",
            "F1.c > 4 or F2.c > 4",
            "F1.c > 1",
            "F1.c < 25",
            "F2.c > 1",
            "F2.c < 25",
            overlap,
        ],
        query_type=QueryType.QUESTION,
        chart_type=ChartType.NORMALIZED_BAR,
        task_types=[
            TaskType.COMPUTE_DERIVED_VALUE
        ],
        description="Shows the frequency (proportion) of one nominal field within each category of another, as a horizontal normalized bar chart.",
        design_considerations="Normalization for proportional comparison. Horizontal layout for higher category counts (>4). Color is preferably mapped to the variable with fewer unique values for better discriminability.",
        tasks="Compare relative proportions across categories; identify which sub-groups dominate in each group.",

    )

    for name, op in [('minimum', Op.min), ('maximum', Op.max), ('average', Op.mean), ('median', Op.median), ('total', Op.sum)]:
        named_aggregate = f"{name} <F1>"
        df = add_row(
            df,
            query_template=f"What is the {name} <F1:q> for each <F2:n>?",
            spec=(
                Chart()
                .source("<E>", "<E.url>")
                .groupby("<F2>")
                .rollup({named_aggregate: op("<F1>")})
                .mark("bar")
                .x(field=named_aggregate, type="quantitative")
                .y(field="<F2>", type="nominal")
            ),
            constraints=[
                "F1.c > 10",
                "F2.c * 2 < E.c",
                "F2.c > 4",
                "F2.c < 25",
                overlap,
            ],
            query_type=QueryType.QUESTION,
            chart_type=ChartType.BARCHART,
            task_types=[
                TaskType.COMPUTE_DERIVED_VALUE
            ],
            description=f"Computes the {name} of a quantitative field for each category, displayed as a horizontal bar chart.",
            design_considerations=f"Horizontal orientation for many categories (>4). Bar length encodes the {name} aggregate value for easy comparison.",
            tasks=f"Compare the {name} value across categories; identify which group has the highest or lowest {name}.",

        )

        df = add_row(
            df,
            query_template=f"What is the {name} <F1:q> for each <F2:n>?",
            spec=(
                Chart()
                .source("<E>", "<E.url>")
                .groupby("<F2>")
                .rollup({named_aggregate: op("<F1>")})
                .mark("bar")
                .x(field="<F2>", type="nominal")
                .y(field=named_aggregate, type="quantitative")
            ),
            constraints=[
                "F1.c > 10",
                "F2.c * 2 < E.c",
                "F2.c <= 4",
                "F2.c > 1",
                overlap,
            ],
            query_type=QueryType.QUESTION,
            chart_type=ChartType.BARCHART,
            task_types=[
                TaskType.COMPUTE_DERIVED_VALUE
            ],
            description=f"Computes the {name} of a quantitative field for each category, displayed as a vertical bar chart.",
            design_considerations=f"Vertical orientation for few categories (<=4). Bar height encodes the {name} aggregate value.",
            tasks=f"Compare the {name} value across categories; identify which group has the highest or lowest {name}.",

        )

    scatterplot_constraints=[
        "F1.c > 10",
        "F2.c > 10",
        "E.c < 100000",
        overlap,
    ]
    df = add_row(
        df,
        query_template="Is there a correlation between <F1:q> and <F2:q>?",
        spec=(
            Chart()
            .source("<E>", "<E.url>")
            .mark("point")
            .x(field="<F1>", type="quantitative")
            .y(field="<F2>", type="quantitative")
        ),
        constraints=scatterplot_constraints,
        query_type=QueryType.QUESTION,
        chart_type=ChartType.SCATTERPLOT,
        task_types=[
            TaskType.CORRELATE
        ],
        description="Plots two quantitative fields as a scatterplot to explore their relationship.",
        design_considerations="Point marks on two quantitative axes reveal correlations, clusters, and outliers. Data size capped at 100k rows for rendering performance.",
        tasks="Assess correlation between two variables; identify outliers and clusters.",

    )

    df = add_row(
        df,
        query_template="Make a scatterplot of <F1:q> and <F2:q>?",
        spec=(
            Chart()
            .source("<E>", "<E.url>")
            .mark("point")
            .x(field="<F1>", type="quantitative")
            .y(field="<F2>", type="quantitative")
        ),
        constraints=scatterplot_constraints,
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.SCATTERPLOT,
        task_types=[
            TaskType.CORRELATE,
            TaskType.CLUSTER,
            TaskType.FIND_ANOMALIES,
            TaskType.DETERMINE_RANGE,
            TaskType.FIND_EXTREMUM
        ],
        description="Creates a scatterplot of two quantitative fields.",
        design_considerations="Point marks on quantitative x and y axes. Data size capped at 100k rows for performance.",
        tasks="Assess correlation; identify clusters, outliers, extremes, and the range of both variables.",

    )

    df = add_row(
        df,
        query_template="Make a stacked bar chart of <F1:n> and <F2:n>?",
        spec=(
            Chart()
            .source("<E>", "<E.url>")
            .groupby(['<F1>', '<F2>'])
            .rollup({"count": Op.count()})
            .mark("bar")
            .x(field="<F1>", type="nominal")
            .y(field="count", type="quantitative")
            .color(field="<F2>", type="nominal")
        ),
        constraints=[
            "F1.c * 2 < E.c",
            "F1.c < 25",
            "F1.c > F2.c",
            "1 < F2.c",
            "F2.c < 8",
            "F1.c <= 4",
            overlap,
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.STACKED_BAR,
        task_types=[
            TaskType.COMPUTE_DERIVED_VALUE,
            TaskType.DETERMINE_RANGE
        ],
        description="Creates a vertical stacked bar chart of counts grouped by two nominal fields.",
        design_considerations="Vertical stacked layout for small primary category counts (<=4). Color encodes the secondary field. Color is preferably mapped to the variable with fewer unique values for better discriminability.",
        tasks="Compare group compositions across categories; assess the overall range of counts.",

    )

    df = add_row(
        df,
        query_template="Make a stacked bar chart of <F1:n> and <F2:n>?",
        spec=(
            Chart()
            .source("<E>", "<E.url>")
            .groupby(['<F1>', '<F2>'])
            .rollup({"count": Op.count()})
            .mark("bar")
            .x(field="count", type="quantitative")
            .y(field="<F1>", type="nominal")
            .color(field="<F2>", type="nominal")
        ),
        constraints=[
            "F1.c * 2 < E.c",
            "F1.c < 25",
            "F1.c > F2.c",
            "1 < F2.c",
            "F2.c < 8",
            "F1.c > 4",
            overlap,
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.STACKED_BAR,
        task_types=[
            TaskType.COMPUTE_DERIVED_VALUE,
            TaskType.DETERMINE_RANGE
        ],
        description="Creates a horizontal stacked bar chart of counts grouped by two nominal fields.",
        design_considerations="Horizontal stacked layout for higher primary category counts (>4). Color encodes the secondary field. Color is preferably mapped to the variable with fewer unique values for better discriminability.",
        tasks="Compare group compositions across categories; assess the overall range of counts.",

    )

    df = add_row(
        df,
        query_template="Make a pie chart of <F:n>?",
        spec=(
            Chart()
            .source("<E>", "<E.url>")
            .groupby('<F>')
            .rollup({"frequency": Op.frequency()})
            .mark("arc")
            .theta(field="frequency", type="quantitative")
            .color(field="<F>", type="nominal")
        ),
        constraints=[
            "F.c * 2 < E.c",
            "F.c > 1",
            "F.c < 8",
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CIRCULAR,
        task_types=[
            TaskType.COMPUTE_DERIVED_VALUE,
            TaskType.DETERMINE_RANGE
        ],
        description="Creates a pie chart showing the frequency distribution of a nominal field.",
        design_considerations="Arc marks with theta encoding map frequency to angle. Suitable for fields with few categories (<8) where part-to-whole perception is the goal.",
        tasks="Assess part-to-whole proportions; identify the dominant category.",

    )

    df = add_row(
        df,
        query_template="Make a donut chart of <F:n>?",
        spec=(
            Chart()
            .source("<E>", "<E.url>")
            .groupby('<F>')
            .rollup({"frequency": Op.frequency()})
            .mark("arc")
            .theta(field="frequency", type="quantitative")
            .color(field="<F>", type="nominal")
            .radius(value=60)
            .radius2(value=80)
        ),
        constraints=[
            "F.c * 2 < E.c",
            "F.c > 1",
            "F.c < 8",
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.CIRCULAR,
        task_types=[
            TaskType.COMPUTE_DERIVED_VALUE,
            TaskType.DETERMINE_RANGE
        ],
        description="Creates a donut chart showing the frequency distribution of a nominal field.",
        design_considerations="Donut variant with inner/outer radius creates a hollow center that can improve label readability. Suitable for few categories (<8).",
        tasks="Assess part-to-whole proportions; identify the dominant category.",

    )

    df = add_row(
        df,
        query_template="How many <E> records are there?",
        spec=(
            Chart()
            .source("<E>", "<E.url>")
            .rollup({"<E> Records": Op.count()})
        ),
        constraints=[
            "E.c > 0"
        ],
        query_type=QueryType.QUESTION,
        chart_type=ChartType.TABLE,
        task_types=[
            TaskType.COMPUTE_DERIVED_VALUE
        ],
        description="Counts the total number of records in an entity and displays the result as a single-row table.",
        design_considerations="Simple rollup with no visual encoding beyond the count value. Useful as a quick data quality or size check.",
        tasks="Retrieve the total record count for an entity.",

    )


    df = add_row(
        df,
        query_template="What does the <E> data look like?",
        spec=(
            Chart()
            .source("<E>", "<E.url>")
        ),
        constraints=[
            "E.c > 0"
        ],
        query_type=QueryType.QUESTION,
        chart_type=ChartType.TABLE,
        task_types=[
            TaskType.DETERMINE_RANGE,
        ],
        description="Displays the raw data for an entity as a table for exploration.",
        design_considerations="No aggregation or transformation applied; shows the underlying data as-is.",
        tasks="Explore the raw data; understand field values and ranges.",

    )

    df = add_row(
        df,
        query_template="Make a table of <E>?",
        spec=(
            Chart()
            .source("<E>", "<E.url>")
        ),
        constraints=[
            "E.c > 0"
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.TABLE,
        task_types=[
            TaskType.DETERMINE_RANGE,
            TaskType.RETRIEVE_VALUE,
            TaskType.FIND_ANOMALIES,
            TaskType.FIND_EXTREMUM
        ],
        description="Creates a table displaying the raw data for an entity.",
        design_considerations="No aggregation or transformation; presents the full dataset for manual inspection.",
        tasks="Explore raw data; retrieve specific values; identify anomalies and extremes.",

    )

    df = add_row(
        df,
        query_template="What does the combined data of <E1> and <E2> look like?",
        spec=(
            Chart()
            .source("<E1>", "<E1.url>")
            .source("<E2>", "<E2.url>")
            .join(
                in_name=['<E1>', '<E2>'],
                on=['<E1.r.E2.id.from>', '<E1.r.E2.id.to>'],
                out_name='<E1>__<E2>',
            )
        ),
        constraints=[
            "E1.c > 0",
            "E2.c > 0",
            "E1.r.E2.c.to == 'one'",
        ],
        query_type=QueryType.QUESTION,
        chart_type=ChartType.TABLE,
        task_types=[
            TaskType.DETERMINE_RANGE,
        ],
        description="Joins two related entities and displays the combined data as a table.",
        design_considerations="Cross-entity join enriches the view by combining fields from two related entities. Requires a valid foreign-key relationship.",
        tasks="Explore combined data from two related entities; understand field values across the join.",

    )

    df = add_row(
        df,
        query_template="Make a table that combines <E1> and <E2>.",
        spec=(
            Chart()
            .source("<E1>", "<E1.url>")
            .source("<E2>", "<E2.url>")
            .join(
                in_name=['<E1>', '<E2>'],
                on=['<E1.r.E2.id.from>', '<E1.r.E2.id.to>'],
                out_name='<E1>__<E2>',
            )
        ),
        constraints=[
            "E1.c > 0",
            "E2.c > 0",
            "E1.r.E2.c.to == 'one`'",
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.TABLE,
        task_types=[
            TaskType.DETERMINE_RANGE,
            TaskType.RETRIEVE_VALUE,
            TaskType.FIND_ANOMALIES,
            TaskType.FIND_EXTREMUM
        ],
        description="Creates a table that joins and displays the combined data of two entities.",
        design_considerations="Cross-entity join via foreign key. Presents the full combined dataset for manual inspection.",
        tasks="Explore joined data; retrieve specific values; identify anomalies and extremes.",

    )

    df = add_row(
        df,
        query_template="What <E2> has the most <E1>?",
        spec=(
            Chart()
            .source("<E1>", "<E1.url>")
            .source("<E2>", "<E2.url>")
            .join(
                in_name=['<E1>', '<E2>'],
                on=['<E1.r.E2.id.from>', '<E1.r.E2.id.to>'],
                out_name='<E1>__<E2>',
            )
            .groupby("<E1.r.E2.id.from>")
            .rollup({"<E1> count": Op.count()})
            .orderby("<E1> count", ascending=False)
            .derive({"rank": "rank()"})
            .derive({"most frequent": "d.rank == 1 ? 'yes' : 'no'"})
            .mark("row")
            .x(field="<E1> count", mark="bar", type="quantitative", domain={"min": 0})
            .color(column="<E1> count", mark="bar", field="most frequent", type="nominal", domain=["yes", "no"], range=["#FFA500", "#c6cfd8"])
            .mark("row")
            .text(field="*", mark="text", type="nominal")
        ),
        constraints=[
            "E1.c > 0",
            "E2.c > 0",
            "E1.r.E2.c.from == 'many'",
        ],
        query_type=QueryType.QUESTION,
        chart_type=ChartType.TABLE,
        task_types=[
            TaskType.FIND_EXTREMUM,
            TaskType.RETRIEVE_VALUE,
            TaskType.COMPUTE_DERIVED_VALUE
        ],
        description="Finds which related entity record has the highest count of associated records, displayed as a ranked table with bar indicators.",
        design_considerations="Groups by foreign key, counts, ranks, and highlights the top record with color encoding. Bar marks on the count column provide visual comparison.",
        tasks="Identify the record with the most associated entities; compare counts across records.",

    )


    df = add_row(
        df,
        query_template="What Record in <E> has the largest <F:q>?",
        spec=(
            Chart()
            .source("<E>", "<E.url>")
            .filter("d['<F>'] != null")
            .orderby("<F>", ascending=False)
            .derive({"largest": "rank() == 1 ? 'largest' : 'not'"})
            .mark("row")
            .x(field="<F>", mark="bar", type="quantitative")
            .color(column='<F>', mark='bar', field='largest', type='nominal', domain=['largest', 'not'], range=['#FFA500', 'c6cfd8'])
            .text(field='*', mark='text', type='nominal')
        ),
        constraints=[
            "F.c > 1",
        ],
        query_type=QueryType.QUESTION,
        chart_type=ChartType.TABLE,
        task_types=[
            TaskType.FIND_EXTREMUM,
            TaskType.RETRIEVE_VALUE,
        ],
        description="Finds the record with the largest value in a quantitative field, displayed as a ranked table with bar indicators.",
        design_considerations="Sorts descending by the target field, derives a rank, and highlights the top record with color. Bar marks provide visual magnitude comparison.",
        tasks="Identify the record with the largest value; compare values across records.",

    )

    df = add_row(
        df,
        query_template="What Record in <E2> has the largest <E1> <E1.F:q>?",
        spec=(
            Chart()
            .source("<E1>", "<E1.url>")
            .source("<E2>", "<E2.url>")
            .join(
                in_name=['<E1>', '<E2>'],
                on=['<E1.r.E2.id.from>', '<E1.r.E2.id.to>'],
                out_name='<E1>__<E2>',
            )
            .groupby("<E1.r.E2.id.from>")
            .rollup({"Largest <E1.F>": Op.max('<E1.F>')})
            .filter("d['Largest <E1.F>'] != null")
            .orderby("Largest <E1.F>", ascending=False)
            .derive({"rank": "rank()"})
            .derive({"largest": "d.rank == 1 ? 'yes' : 'no'"})
            .mark("row")
            .x(field="Largest <E1.F>", mark="bar", type="quantitative")
            .color(column="Largest <E1.F>", mark="bar", field="largest", type="nominal", domain=["yes", "no"], range=["#FFA500", "#c6cfd8"])
            .text(field="*", mark="text", type="nominal")
        ),
        constraints=[
            "E1.c > 0",
            "E2.c > 0",
            "E1.r.E2.c.from == 'many'",
            "E1.F.name not in E2.fields",
        ],
        query_type=QueryType.QUESTION,
        chart_type=ChartType.TABLE,
        task_types=[
            TaskType.FIND_EXTREMUM,
            TaskType.RETRIEVE_VALUE,
            TaskType.COMPUTE_DERIVED_VALUE
        ],
        description="Joins two entities, computes the maximum of a quantitative field per group, and ranks the results in a table with bar indicators.",
        design_considerations="Cross-entity join followed by group-level max aggregation. Highlights the top record with color encoding. Useful when the extremum requires aggregation across a relationship.",
        tasks="Identify which related record has the largest aggregated value; compare across groups.",

    )

    df = add_row(
        df,
        query_template="What Record in <E> has the smallest <F:q>?",
        spec=(
            Chart()
            .source("<E>", "<E.url>")
            .filter("d['<F>'] != null")
            .orderby("<F>")
            .derive({"smallest": "rank() == 1 ? 'smallest' : 'not'"})
            .mark("row")
            .color(column='<F>', mark='rect', orderby='<F>', field='smallest', type='nominal', domain=['smallest', 'not'], range=['#ffdb9a', 'white'])
            .text(field='*', mark='text', type='nominal')
        ),
        constraints=[
            "F.c > 1",
        ],
        query_type=QueryType.QUESTION,
        chart_type=ChartType.TABLE,
        task_types=[
            TaskType.FIND_EXTREMUM,
            TaskType.RETRIEVE_VALUE,
        ],
        description="Finds the record with the smallest value in a quantitative field, displayed as a ranked table with conditional formatting.",
        design_considerations="Sorts ascending by the target field, derives a rank, and highlights the top record with background color. Uses rect mark for row-level highlighting.",
        tasks="Identify the record with the smallest value; compare values across records.",

    )

    df = add_row(
        df,
        query_template="What Record in <E2> has the smallest <E1> <E1.F:q>?",
        spec=(
            Chart()
            .source("<E1>", "<E1.url>")
            .source("<E2>", "<E2.url>")
            .join(
                in_name=['<E1>', '<E2>'],
                on=['<E1.r.E2.id.from>', '<E1.r.E2.id.to>'],
                out_name='<E1>__<E2>',
            )
            .groupby("<E1.r.E2.id.from>")
            .rollup({"Smallest <E1.F>": Op.min('<E1.F>')})
            .filter("d['Smallest <E1.F>'] != null")
            .orderby("Smallest <E1.F>", ascending=True)
            .derive({"rank": "rank()"})
            .derive({"smallest": "d.rank == 1 ? 'yes' : 'no'"})
            .mark("row")
            .color(column="Smallest <E1.F>", mark="bar", orderby="Smallest <E1.F>", field="smallest", type="nominal", domain=["yes", "no"], range=["#ffdb9a", "white"])
            .text(field="*", mark="text", type="nominal")
        ),
        constraints=[
            "E1.c > 0",
            "E2.c > 0",
            "E1.r.E2.c.from == 'many'",
            "E1.F.name not in E2.fields",
        ],
        query_type=QueryType.QUESTION,
        chart_type=ChartType.TABLE,
        task_types=[
            TaskType.FIND_EXTREMUM,
            TaskType.RETRIEVE_VALUE,
        ],
        description="Joins two entities, computes the minimum of a quantitative field per group, and ranks the results in a table with conditional formatting.",
        design_considerations="Cross-entity join followed by group-level min aggregation. Highlights the top record with background color via rect mark.",
        tasks="Identify which related record has the smallest aggregated value; compare across groups.",

    )

    df = add_row(
        df,
        query_template="Order the <E> by <F:q>?",
        spec=(
            Chart()
            .source("<E>", "<E.url>")
            .filter("d['<F>'] != null")
            .orderby("<F>")
            .mark("row")
            .x(column='<F>', mark='bar', field='<F>', type='quantitative', range={'min': 0.2, 'max': 1})
            .text(field='*', mark='text', type='nominal')
        ),
        constraints=[
            "F.c > 1",
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.TABLE,
        task_types=[
            TaskType.SORT,
        ],
        description="Sorts entity records by a quantitative field and displays the result as an ordered table with in-cell bar marks.",
        design_considerations="Ordered by the quantitative field with nulls filtered out. In-cell bar marks provide visual comparison of magnitude alongside the text values.",
        tasks="View records in sorted order; compare relative magnitudes.",

    )


    df = add_row(
        df,
        query_template="What is the range of <E> <F:q> values?",
        spec=(
            Chart()
            .source("<E>", "<E.url>")
            .filter("d['<F>'] != null")
            .rollup({
                "<F> min": Op.min("<F>"),
                "<F> max": Op.max("<F>")
            })
            .mark("row")
            .text(field="<F> min", mark='text', type='nominal')
            .text(field="<F> max", mark='text', type='nominal')
        ),
        constraints=[
            "F.c > 1",
        ],
        query_type=QueryType.QUESTION,
        chart_type=ChartType.TABLE,
        task_types=[
            TaskType.DETERMINE_RANGE,
        ],
        description="Computes the minimum and maximum of a quantitative field and displays them as a single-row table.",
        design_considerations="Simple rollup of min and max. Filters out nulls before aggregation for accuracy.",
        tasks="Determine the range of a quantitative field.",

    )

    df = add_row(
        df,
        query_template="What is the range of <E> <F:n> values?",
        spec=(
            Chart()
            .source("<E>", "<E.url>")
            .filter("d['<F>'] != null")
            .groupby("<F>")
            .rollup({ "count": Op.count() })
            .mark("row")
            .text(field="<F>", mark='text', type='nominal')
            .x(field="count", mark='bar', type='quantitative', range={'min': 0.1, 'max': 1})
        ),
        constraints=[
            "F.c > 1",
            "F.c < 50",
        ],
        query_type=QueryType.QUESTION,
        chart_type=ChartType.TABLE,
        task_types=[
            TaskType.DETERMINE_RANGE,
        ],
        description="Lists all distinct values of a nominal field with their counts, displayed as a table with in-cell bar marks.",
        design_considerations="Groups by the nominal field and counts occurrences. In-cell bars provide visual frequency comparison. Limits to fields with fewer than 50 categories.",
        tasks="Determine the range (distinct values) of a nominal field; compare category frequencies.",

    )

    df = add_row(
        df,
        query_template="What is the range of <E> <F1:q> values for every <F2:n>?",
        spec=(
            Chart()
            .source("<E>", "<E.url>")
            .filter("d['<F1>'] != null")
            .groupby("<F2>")
            .rollup({
                "<F1> min": Op.min("<F1>"),
                "<F1> max": Op.max("<F1>")
            })
            .derive({"range": "d['<F1> max'] - d['<F1> min']"})
            .orderby("range", ascending=False)
            .mark("row")
            .text(field="<F2>", mark='text', type='nominal')
            .text(field="<F1> min", mark='text', type='nominal')
            .x(column="range", mark='bar', field="<F1> min", type='quantitative', domain={"numberFields": ["<F1> min", "<F1> max"]})
            .x2(column="range", mark='bar', field="<F1> max", type='quantitative', domain={"numberFields": ["<F1> min", "<F1> max"]})
            .text(field="<F1> max", mark='text', type='nominal')
        ),
        constraints=[
            "F1.c > 1",
            "F2.c > 1",
            "F2.c < F1.c",
            overlap,
        ],
        query_type=QueryType.QUESTION,
        chart_type=ChartType.TABLE,
        task_types=[
            TaskType.DETERMINE_RANGE,
        ],
        description="Computes the min and max of a quantitative field for each category of a nominal field, displayed as a table with range bar marks.",
        design_considerations="Groups by nominal field, computes min/max and derived range, then orders by range descending. Uses x/x2 encoding to show the span between min and max values.",
        tasks="Compare the spread of a quantitative field across categories; identify which group has the widest or narrowest range.",

    )

    df = add_row(
        df,
        query_template="What is the most frequent <F:n>?",
        spec=(
            Chart()
            .source("<E>", "<E.url>")
            .filter("d['<F>']")
            .groupby("<F>")
            .rollup({"count": Op.count()})
            .orderby("count", ascending=False)
            .derive({"rank": "rank()"})
            .derive({"most frequent": "d.rank == 1 ? 'yes' : 'no'"})
            .mark("row")
            .color(column="<F>", mark="bar", orderby="<F>", field="most frequent", type="nominal", domain=["yes", "no"], range=["#ffdb9a", "white"])
            .text(field="<F>", mark="text", type="nominal")
            .x(field="count", mark="bar", type="quantitative", domain={"min": 0})
            .color(column="count", mark="bar", field="most frequent", type="nominal", domain=["yes", "no"], range=["#FFA500", "#c6cfd8"])
        ),
        constraints=[
            "F.c * 2 < E.c",
            "F.c > 1",
        ],
        query_type=QueryType.QUESTION,
        chart_type=ChartType.TABLE,
        task_types=[
            TaskType.FIND_EXTREMUM,
            TaskType.RETRIEVE_VALUE,
            TaskType.COMPUTE_DERIVED_VALUE
        ],
        description="Finds the most frequent value of a nominal field, displayed as a ranked table with bar marks and conditional formatting.",
        design_considerations="Groups by nominal field, counts, ranks, and highlights the top value. Combines bar marks for count comparison and background color for emphasis.",
        tasks="Identify the most frequent category; compare frequencies across all categories.",

    )

    df = add_row(
        df,
        query_template="What is the cumulative distribution of <F:q>?",
        spec=(
            Chart()
            .source("<E>", "<E.url>")
            .filter("d['<F>'] != null")
            .orderby("<F>")
            .derive({ "total": "count()" })
            .derive({"percentile": rolling("count() / d.total")})
            .mark("line")
            .x(field="<F>", type="quantitative")
            .y(field="percentile", type="quantitative")
        ),
        constraints=[
            "F.c > 10",
        ],
        query_type=QueryType.QUESTION,
        chart_type=ChartType.LINE,
        task_types=[
            TaskType.CHARACTERIZE_DISTRIBUTION,
        ],
        description="Shows the cumulative distribution function (CDF) of a quantitative field as a line chart.",
        design_considerations="Sorts by value, computes rolling percentile, and draws a line. The CDF reveals the full distribution shape including median, quartiles, and tails.",
        tasks="Characterize the distribution of a variable; identify median, quartiles, and concentration of values.",

    )

    df = add_row(
        df,
        query_template="Make a CDF plot of <F:q>.",
        spec=(
            Chart()
            .source("<E>", "<E.url>")
            .filter("d['<F>'] != null")
            .orderby("<F>")
            .derive({ "total": "count()" })
            .derive({"percentile": rolling("count() / d.total")})
            .mark("line")
            .x(field="<F>", type="quantitative")
            .y(field="percentile", type="quantitative")
        ),
        constraints=[
            "F.c > 10",
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.LINE,
        task_types=[
            TaskType.CHARACTERIZE_DISTRIBUTION,
        ],
        description="Creates a CDF (cumulative distribution function) plot of a quantitative field.",
        design_considerations="Sorts values, computes cumulative percentile, and renders as a line chart.",
        tasks="Characterize the distribution of a variable; identify median, quartiles, and concentration of values.",

    )

    df = add_row(
        df,
        query_template="What is the cumulative distribution of <F1:q> for each <F2:n>?",
        spec=(
            Chart()
            .source("<E>", "<E.url>")
            .filter("d['<F1>'] != null")
            .orderby("<F1>")
            .groupby("<F2>")
            .derive({ "total": "count()" })
            .derive({"percentile": rolling("count() / d.total")})
            .mark("line")
            .x(field="<F1>", type="quantitative")
            .y(field="percentile", type="quantitative")
            .color(field="<F2>", type="nominal")
        ),
        constraints=[
            "F1.c > 10",
            "F2.c > 1",
            "F2.c < 5",
            overlap,
        ],
        query_type=QueryType.QUESTION,
        chart_type=ChartType.GROUPED_LINE,
        task_types=[
            TaskType.CHARACTERIZE_DISTRIBUTION,
        ],
        description="Shows the cumulative distribution of a quantitative field for each category of a nominal field, with separate lines per group.",
        design_considerations="Groups by nominal field before computing per-group CDF. Color encodes group identity. Limited to fewer than 5 groups for readability.",
        tasks="Compare distributions across groups; identify which groups have higher or lower concentrations of values.",

    )

    df = add_row(
        df,
        query_template="Make a CDF plot of <F1:q> with a line for each <F2:n>.",
        spec=(
            Chart()
            .source("<E>", "<E.url>")
            .filter("d['<F1>'] != null")
            .orderby("<F1>")
            .groupby("<F2>")
            .derive({ "total": "count()" })
            .derive({"percentile": rolling("count() / d.total")})
            .mark("line")
            .x(field="<F1>", type="quantitative")
            .y(field="percentile", type="quantitative")
            .color(field="<F2>", type="nominal")
        ),
        constraints=[
            "F1.c > 10",
            "F2.c > 1",
            "F2.c < 5",
            overlap,
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.GROUPED_LINE,
        task_types=[
            TaskType.CHARACTERIZE_DISTRIBUTION,
        ],
        description="Creates a CDF plot with a separate line for each category of a nominal field.",
        design_considerations="Per-group CDF computation with color encoding to distinguish groups. Limited to fewer than 5 groups.",
        tasks="Compare distributions across groups; identify which groups have higher or lower concentrations of values.",

    )

    df = add_row(
        df,
        query_template=f"Are there any clusters with respect to <E> counts of <F1:n> and <F2:n>?",
        spec=(
            Chart()
            .source("<E>", "<E.url>")
            .groupby(["<F2>", "<F1>"])
            .rollup({"count <E>": Op.count()})
            .derive({"udi_internal_percentile": "d['count <E>'] / max(d['count <E>'])"})
            .derive({"udi_internal_text_color_threshold": "d.udi_internal_percentile > .5 ? 'large' : 'small'"})
            .mark("rect")
            .color(field="count <E>", type="quantitative")
            .y(field="<F1>", type="nominal")
            .x(field="<F2>", type="nominal")
            .mark("text")
            .text(field="count <E>", type="quantitative")
            .y(field="<F1>", type="nominal")
            .x(field="<F2>", type="nominal")
            .color(field="udi_internal_text_color_threshold", type="nominal", domain=["large", "small"], range=["white", "black"], omitLegend=True)
        ),
        constraints=[
            "F1.c * 2 < E.c",
            "F2.c * 2 < E.c",
            "F1.c > 1",
            "F2.c > 1",
            "F1.c <= 30",
            "F2.c <= 30",
            "F1.c >= F2.c",
            overlap,
        ],
        query_type=QueryType.QUESTION,
        chart_type=ChartType.HEATMAP,
        task_types=[
            TaskType.CLUSTER,
        ],
        description="Displays the count of entities for each combination of two nominal fields as a heatmap with labeled cells.",
        design_considerations="Rect marks with quantitative color encoding show density. Overlaid text marks display exact counts. Text color adapts based on cell intensity for readability. The field with more unique values is preferably placed on the y-axis, where longer labels remain readable.",
        tasks="Identify clusters or patterns in the co-occurrence of two fields; find the most and least common combinations.",

    )

    df = add_row(
        df,
        query_template=f"Make a heatmap of <E> <F1:n> and <F2:n>.",
        spec=(
            Chart()
            .source("<E>", "<E.url>")
            .groupby(["<F2>", "<F1>"])
            .rollup({"count <E>": Op.count()})
            .derive({"udi_internal_percentile": "d['count <E>'] / max(d['count <E>'])"})
            .derive({"udi_internal_text_color_threshold": "d.udi_internal_percentile > .5 ? 'large' : 'small'"})
            .mark("rect")
            .color(field="count <E>", type="quantitative")
            .y(field="<F1>", type="nominal")
            .x(field="<F2>", type="nominal")
            .mark("text")
            .text(field="count <E>", type="quantitative")
            .y(field="<F1>", type="nominal")
            .x(field="<F2>", type="nominal")
            .color(field="udi_internal_text_color_threshold", type="nominal", domain=["large", "small"], range=["white", "black"], omitLegend=True)
        ),
        constraints=[
            "F1.c * 2 < E.c",
            "F2.c * 2 < E.c",
            "F1.c > 1",
            "F2.c > 1",
            "F1.c <= 30",
            "F2.c <= 30",
            "F1.c >= F2.c",
            overlap,
        ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.HEATMAP,
        task_types=[
            TaskType.CLUSTER,
            TaskType.COMPUTE_DERIVED_VALUE,
            TaskType.CORRELATE
        ],
        description="Creates a heatmap showing entity counts for each combination of two nominal fields.",
        design_considerations="Rect marks with color encoding and text labels. Text color adapts to background intensity. Both axes limited to 30 or fewer categories. The field with more unique values is preferably placed on the y-axis for better label readability.",
        tasks="Identify clusters and patterns; compare counts across combinations; find correlations between two fields.",

    )


    # Heatmap of aggregates over two nominal fields.
    for name, op in [('average', Op.mean)]:
            named_aggregate = f"{name} <F1>"
            df = add_row(
                df,
                query_template=f"What is the {name} <F1:q> for each <F2:n> and <F3:n>?",
                
                spec=(
                    Chart()
                    .source("<E>", "<E.url>")
                    .groupby(["<F3>", "<F2>"])
                    .rollup({named_aggregate: op("<F1>")})
                    .mark("rect")
                    .color(field=named_aggregate, type="quantitative")
                    .y(field="<F2>", type="nominal")
                    .x(field="<F3>", type="nominal")
                ),
                constraints=[
                    "F1.c > 100",
                    "F2.c * 2 < E.c",
                    "F3.c * 2 < E.c",
                    "F2.c > 1",
                    "F2.c < 25",
                    "F3.c > 1",
                    "F3.c < 25",
                    "F2.c >= F3.c",
                    overlap,
                    "F1['name'] in F3['udi:overlapping_fields'] or F3['udi:overlapping_fields'] == 'all'",
                    "F2['name'] in F3['udi:overlapping_fields'] or F3['udi:overlapping_fields'] == 'all'"
                ],
                query_type=QueryType.QUESTION,
                chart_type=ChartType.HEATMAP,
                task_types=[
                    TaskType.CLUSTER,
                    TaskType.COMPUTE_DERIVED_VALUE,
                    TaskType.CORRELATE
                ],
                description=f"Displays the {name} of a quantitative field for each combination of two nominal fields as a heatmap.",
                design_considerations=f"Uses three fields: a quantitative measure aggregated by {name}, and two nominal axes. Color encodes the aggregate value. Requires overlapping fields across all three. The field with more unique values is preferably placed on the y-axis for better label readability.",
                tasks=f"Identify patterns in the {name} value across two categorical dimensions; find combinations with extreme values.",

            )


    # scatterplot with color
    df = add_row(
        df,
        query_template="Are there clusters of <E> <F1:q> and <F2:q> values across different <F3:n> groups?",
        spec=(
            Chart()
            .source("<E>", "<E.url>")
            .mark("point")
            .x(field="<F1>", type="quantitative")
            .y(field="<F2>", type="quantitative")
            .color(field="<F3>", type="nominal")
        ),
        constraints=[
            "F1.c > 10",
            "F2.c > 10",
            "F3.c > 1",
            "F3.c < 8",
            overlap,
            "F1['name'] in F3['udi:overlapping_fields'] or F3['udi:overlapping_fields'] == 'all'",
            "F2['name'] in F3['udi:overlapping_fields'] or F3['udi:overlapping_fields'] == 'all'"
        ],
        query_type=QueryType.QUESTION,
        chart_type=ChartType.GROUPED_SCATTER,
        task_types=[
            TaskType.CLUSTER,
        ],
        description="Plots two quantitative fields as a scatterplot with points colored by a nominal field to reveal group-level clusters.",
        design_considerations="Adds color encoding to a standard scatterplot to separate groups visually. Limited to fewer than 8 color categories for perceptual clarity.",
        tasks="Identify clusters that separate by group; assess whether the relationship between two quantitative fields differs across groups.",

    )

    # Histogram
    df = add_row(
        df,
        query_template="What is the distribution of <F:q>?",
        spec=(
            Chart()
            .source("<E>", "<E.url>")
            .filter("d['<F>'] != null")
            .binby(
                field="<F>", 
                output={
                    "bin_start": "start",
                    "bin_end": "end"})
            .rollup({"count": Op.count()})
            .mark("rect")
            .x(field="start", type="quantitative")
            .x2(field="end", type="quantitative")
            .y(field="count", type="quantitative")
        ),
        constraints=[
            "F.c > 250",
            ],
        query_type=QueryType.QUESTION,
        chart_type=ChartType.HISTOGRAM,
        task_types=[
            TaskType.CHARACTERIZE_DISTRIBUTION,
        ],
        description="Shows the distribution of a quantitative field as a histogram with automatically computed bins.",
        design_considerations="Uses binby to create equal-width bins. Rect marks span from bin start to bin end on x, with count on y. Requires high cardinality (>250) to ensure meaningful binning.",
        tasks="Characterize the shape of a distribution; identify modes, skewness, and gaps.",

    )

    df = add_row(
        df,
        query_template="Make a histogram of <F:q>?",
        spec=(
            Chart()
            .source("<E>", "<E.url>")
            .filter("d['<F>'] != null")
            .binby(
                field="<F>", 
                output={
                    "bin_start": "start",
                    "bin_end": "end"})
            .rollup({"count": Op.count()})
            .mark("rect")
            .x(field="start", type="quantitative")
            .x2(field="end", type="quantitative")
            .y(field="count", type="quantitative")
        ),
        constraints=[
            "F.c > 5",
            ],
        query_type=QueryType.UTTERANCE,
        chart_type=ChartType.HISTOGRAM,
        task_types=[
            TaskType.CHARACTERIZE_DISTRIBUTION,
        ],
        description="Creates a histogram of a quantitative field with automatically computed bins.",
        design_considerations="Uses binby for automatic bin computation. Rect marks show bin ranges and counts. Lower cardinality threshold (>5) than the question variant.",
        tasks="Characterize the shape of a distribution; identify modes, skewness, and gaps.",

    )

    # KDE
    df = add_row(
        df,
        query_template="What is the distribution of <F:q>?",
        spec=(
            Chart()
            .source("<E>", "<E.url>")
            .filter("d['<F>'] != null")
            .kde(
                field="<F>", 
                output={
                    "sample": "<F>",
                    "density": "density"},)
            .mark("area")
            .x(field="<F>", type="quantitative")
            .y(field="density", type="quantitative")
        ),
        constraints=[
            "F.c > 50",
            "F.c <= 250",
        ],
        query_type=QueryType.QUESTION,
        chart_type=ChartType.AREA,
        task_types=[
            TaskType.CHARACTERIZE_DISTRIBUTION,
        ],
        description="Shows the distribution of a quantitative field as a smooth density curve (KDE) rendered as an area chart.",
        design_considerations="Kernel density estimation produces a smooth curve. Area mark fills below the density line. Used for moderate cardinality (50-250) where a smooth estimate is more informative than binning.",
        tasks="Characterize the shape of a distribution; identify modes and overall density patterns.",

    )

    # Dot plot
    df = add_row(
        df,
        query_template="What is the distribution of <F:q>?",
        spec=(
            Chart()
            .source("<E>", "<E.url>")
            .mark("point")
            .x(field="<F>", type="quantitative")
        ),
        constraints=[
            "F.c > 1",
            "F.c <= 50",
        ],
        query_type=QueryType.QUESTION,
        chart_type=ChartType.DOT,
        task_types=[
            TaskType.CHARACTERIZE_DISTRIBUTION,
        ],
        description="Shows the distribution of a quantitative field as individual points along a single axis.",
        design_considerations="Point marks on a single quantitative x-axis. Best for small datasets (50 or fewer values) where individual observations are meaningful and overplotting is minimal.",
        tasks="Characterize the distribution; identify individual values, clusters, and outliers.",

    )


    df = add_row(
        df,
        query_template="Is the distribution of <F1:q> similar for each <F2:n>?",
        spec=(
            Chart()
            .source("<E>", "<E.url>")
            .filter("d['<F1>'] != null")
            .groupby("<F2>")
            .kde(
                field="<F1>", 
                output={
                    "sample": "<F1>",
                    "density": "density"},)
            .mark("area")
            .x(field="<F1>", type="quantitative")
            .color(field="<F2>", type="nominal")
            .y(field="density", type="quantitative")
            .opacity(value=0.25)
            .mark('line')
            .x(field="<F1>", type="quantitative")
            .color(field="<F2>", type="nominal")
            .y(field="density", type="quantitative")
        ),
        constraints=[
            "F1.c > 50",
            "F1.c < 250",
            "F2.c < 4",
            overlap,
        ],
        query_type=QueryType.QUESTION,
        chart_type=ChartType.GROUPED_AREA,
        task_types=[
            TaskType.CHARACTERIZE_DISTRIBUTION,
        ],
        description="Compares the distribution of a quantitative field across categories using overlapping density curves (KDE) with area and line marks.",
        design_considerations="Per-group KDE with semi-transparent area fills and line outlines. Color encodes group identity. Limited to fewer than 4 groups to avoid excessive overlap. Opacity set to 0.25 for layering.",
        tasks="Compare distribution shapes across groups; identify shifts in central tendency or spread.",

    )

    df = add_row(
        df,
        query_template="Is the distribution of <F1:q> similar for each <F2:n>?",
        spec=(
            Chart()
            .source("<E>", "<E.url>")
            .mark("point")
            .x(field="<F1>", type="quantitative")
            .y(field="<F2>", type="nominal")
            .color(field="<F2>", type="nominal")
        ),
        constraints=[
            "F1.c > 1",
            "F1.c <= 50",
            "F2.c < 8",
            overlap,
        ],
        query_type=QueryType.QUESTION,
        chart_type=ChartType.GROUPED_DOT,
        task_types=[
            TaskType.CHARACTERIZE_DISTRIBUTION,
        ],
        description="Compares the distribution of a quantitative field across categories using dot strips, with one row per category.",
        design_considerations="Points plotted on a quantitative x-axis with nominal y-axis for group separation. Color reinforces group identity. Best for small datasets (50 or fewer values per group).",
        tasks="Compare distributions across groups; identify clusters and outliers within each group.",

    )

    df = add_row(
        df,
        query_template="How many <E> records have a non-null <F:q|o|n>?",
        spec=(
            Chart()
            .source("<E>", "<E.url>")
            .derive({"<E> Count": "count()"})
            .filter("d['<F>'] != null")
            .rollup({
                "Valid <F> Count": Op.count(),
                "<E> Count": Op.median("<E> Count")
            })
            .derive({"Valid <F> %": "d['Valid <F> Count'] / d['<E> Count']"})
            .mark("row")
            .text(field="Valid <F> Count", mark='text', type='nominal')
            .text(field="<E> Count", mark='text', type='nominal')
            .x(field="Valid <F> %", mark='bar', type='quantitative', domain={"min": 0, "max": 1})
            .y(field="Valid <F> %", mark='line', type='quantitative', range={"min": 0.5, "max": 0.5})
        ),
        constraints=[
            "E.c > 0",
            "F.c > 0",
        ],
        query_type=QueryType.QUESTION,
        chart_type=ChartType.TABLE,
        task_types=[
            TaskType.FILTER,
            TaskType.COMPUTE_DERIVED_VALUE
        ],
        description="Counts the number of records with a non-null value in a specified field, shown alongside the total with a percentage bar.",
        design_considerations="Derives total count before filtering, then filters to non-null and counts valid records. Percentage bar and 50%% reference line provide visual context for data completeness.",
        tasks="Assess data completeness for a field; determine how many records have valid values.",

    )

    df = add_row(
        df,
        query_template="What percentage of <E> records have a non-null <F:q|o|n>?",
        spec=(
            Chart()
            .source("<E>", "<E.url>")
            .derive({"<E> Count": "count()"})
            .filter("d['<F>'] != null")
            .rollup({
                "Valid <F> Count": Op.count(),
                "<E> Count": Op.median("<E> Count")
            })
            .derive({"Valid <F> %": "d['Valid <F> Count'] / d['<E> Count']"})
            .mark("row")
            .text(field="Valid <F> Count", mark='text', type='nominal')
            .text(field="<E> Count", mark='text', type='nominal')
            .x(field="Valid <F> %", mark='bar', type='quantitative', domain={"min": 0, "max": 1})
            .y(field="Valid <F> %", mark='line', type='quantitative', range={"min": 0.5, "max": 0.5})
        ),
        constraints=[
            "E.c > 0",
            "F.c > 0",
        ],
        query_type=QueryType.QUESTION,
        chart_type=ChartType.TABLE,
        task_types=[
            TaskType.FILTER,
            TaskType.COMPUTE_DERIVED_VALUE
        ],
        description="Computes the percentage of records with a non-null value in a specified field, shown with a percentage bar.",
        design_considerations="Same computation as non-null count but framed as a percentage question. Percentage bar with 50%% reference line aids interpretation.",
        tasks="Assess data completeness as a proportion; determine what fraction of records have valid values.",

    )

    df = add_row(
        df,
        query_template="How many <E> records have a null <F:q|o|n>?",
        spec=(
            Chart()
            .source("<E>", "<E.url>")
            .derive({"<E> Count": "count()"})
            .filter("d['<F>'] != null")
            .rollup({
                "Valid <F> Count": Op.count(),
                "<E> Count": Op.median("<E> Count")
            })
            .derive({
                "Null <F> Count": "d['<E> Count'] - d['Valid <F> Count']",
                "Null <F> %": "1 - d['Valid <F> Count'] / d['<E> Count']"
            })
            .mark("row")
            .text(field="Null <F> Count", mark='text', type='nominal')
            .text(field="<E> Count", mark='text', type='nominal')
            .x(field="Null <F> %", mark='bar', type='quantitative', domain={"min": 0, "max": 1})
            .y(field="Null <F> %", mark='line', type='quantitative', range={"min": 0.5, "max": 0.5})
        ),
        constraints=[
            "E.c > 0",
            "F.c > 0",
        ],
        query_type=QueryType.QUESTION,
        chart_type=ChartType.TABLE,
        task_types=[
            TaskType.FILTER,
            TaskType.COMPUTE_DERIVED_VALUE
        ],
        description="Counts the number of records with a null value in a specified field, shown alongside the total with a percentage bar.",
        design_considerations="Derives null count as total minus valid count. Percentage bar shows the null proportion with a 50%% reference line.",
        tasks="Assess data quality; determine how many records are missing a value.",

    )

    df = add_row(
        df,
        query_template="What percentage of <E> records have a null <F:q|o|n>?",
        spec=(
            Chart()
            .source("<E>", "<E.url>")
            .derive({"<E> Count": "count()"})
            .filter("d['<F>'] != null")
            .rollup({
                "Valid <F> Count": Op.count(),
                "<E> Count": Op.median("<E> Count")
            })
            .derive({
                "Null <F> Count": "d['<E> Count'] - d['Valid <F> Count']",
                "Null <F> %": "1 - d['Valid <F> Count'] / d['<E> Count']"
            })
            .mark("row")
            .text(field="Null <F> Count", mark='text', type='nominal')
            .text(field="<E> Count", mark='text', type='nominal')
            .x(field="Null <F> %", mark='bar', type='quantitative', domain={"min": 0, "max": 1})
            .y(field="Null <F> %", mark='line', type='quantitative', range={"min": 0.5, "max": 0.5})
        ),
        constraints=[
            "E.c > 0",
            "F.c > 0",
        ],
        query_type=QueryType.QUESTION,
        chart_type=ChartType.TABLE,
        task_types=[
            TaskType.FILTER,
            TaskType.COMPUTE_DERIVED_VALUE
        ],
        description="Computes the percentage of records with a null value in a specified field, shown with a percentage bar.",
        design_considerations="Same computation as null count but framed as a percentage. Percentage bar visualizes the null proportion.",
        tasks="Assess data quality as a proportion; determine what fraction of records are missing a value.",

    )

    return df


if __name__ == "__main__":
    import os

    os.makedirs('./out', exist_ok=True)
    df = generate()

    # Serialize task_types enum values to strings
    df['task_types'] = df['task_types'].apply(lambda x: [t.value for t in x])

    print(f"Generated {len(df)} templates.")
    print(f"\nColumns: {list(df.columns)}")
    print(f"\nChart types: {df['chart_type'].value_counts().to_dict()}")
    print(f"Query types: {df['query_type'].value_counts().to_dict()}")
    print(f"Complexity: {df['chart_complexity'].value_counts().to_dict()}")

    df.to_json('./out/templates.json', orient='records', indent=2)
    print(f"\nExported to ./out/templates.json")
