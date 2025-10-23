import json
import pandas as pd
from datasets import load_dataset
dataset = load_dataset(f"HIDIVE/DQVis")
df = dataset['train'].to_pandas()

# fitler df to only include dataset_schema of hubmap_2025-05-05
df = df[df['dataset_schema'].isin(['hubmap_2025-05-05'])]
# TODO: get other dataset_schemas working

# group by the combination of query_template and spec_template
grouped = df.groupby(['query_template', 'spec_template', 'dataset_schema'])

# randomly sample one row from each group
# set random_state for reproducibility
sampled_df = grouped.apply(lambda x: x.sample(1, random_state=97930)).reset_index(drop=True)
print(sampled_df)

# get data package map
data_package_map = {
    "4DN": "./out/data_packages/4DN/datapackage_udi.json",
    "hubmap_2025-05-05": "./out/data_domains/hubmap_data_schema.json",
    "MetabolomicsWorkbench": "./out/data_packages/MetabolomicsWorkbench/C2M2_datapackage_udi.json",
    "MoTrPAC": "./out/data_packages/MoTrPAC/C2M2_datapackage_udi.json",
    "SenNet": "./out/data_packages/SenNet/C2M2_datapackage_udi.json",
}
# convert paths to content
for key, path in data_package_map.items():
    with open(path, 'r') as f:
        content = json.load(f)
        data_package_map[key] = json.dumps(content)

# get data domain map
data_domain_map = {
    "4DN": "./out/data_domains/4DN_domains.json",
    "hubmap_2025-05-05": "./out/data_domains/hubmap_domains.json",
    "MetabolomicsWorkbench": "./out/data_domains/MetabolomicsWorkbench_domains.json",
    "MoTrPAC": "./out/data_domains/MoTrPac_domains.json",
    "SenNet": "./out/data_domains/SenNet_domains.json",
}
# convert paths to content
for key, path in data_domain_map.items():
    with open(path, 'r') as f:
        content = f.read()
        data_domain_map[key] = content

test_case_list = []
for index, row in sampled_df.iterrows():
    test_case = {
        "input": {
            "model": "agenticx/UDI-VIS-Beta-v2-Llama-3.1-8B",
            "messages": [
                {
                    "role": "user",
                    "content": row['query']
                }
            ],
            "dataSchema": data_package_map.get(row['dataset_schema'], ""),
            "dataDomains":  data_domain_map.get(row['dataset_schema'], ""),
        },
        "expected": {
            "tool_calls": [
                {
                    "name": 'RenderVisualization',
                    "arguments": {
                        "spec": row['spec']
                    }
                }
            ],
            "orchestrator_choice": 'render-visualization'
        },
    }
    test_case_list.append(test_case)


# save to json file
import json
with open('./out/benchmark_sample.json', 'w') as f:
    json.dump(test_case_list, f, indent=4)