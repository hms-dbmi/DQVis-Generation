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


def add_row(df, query_template, spec, constraints, query_type: QueryType, chart_type: ChartType, task_types: list[TaskType]):
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
        "task_types": task_types
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
            "task_types"
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
        ]
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
        ]
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
        ]
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
        ]
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
        ]
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
        ]
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
        ]
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
        ]
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
        ]
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
        ]
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
        ]
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
        ]
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
        ]
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
        ]
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
        ]
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
            ]
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
            ]
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
        ]
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
        ]
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
        ]
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
        ]
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
        ]
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
        ]
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
        ]
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
        ]
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
        ]
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
        ]
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
        ]
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
        ]
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
        ]
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
        ]
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
        ]
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
        ]
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
        ]
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
        ]
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
        ]
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
        ]
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
        ]
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
        ]
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
        ]
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
        ]
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
        ]
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
        ]
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
        ]
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
                ]
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
        ]
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
        ]
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
        ]
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
        ]
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
        ]
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
        ]
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
        ]
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
        ]
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
        ]
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
        ]
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
        ]
    )

    return df


if __name__ == "__main__":
    df = generate()
    print(df.head())
