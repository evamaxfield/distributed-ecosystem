#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
To run this example and generate the flow-viz.png file in static/

Run:
```
conda env create -f environment.yml
conda activate distributed-ecosystem
python example-flow.py
```
"""


from typing import Any, List

import dask.array as da
import pandas as pd
from aicsimageio import AICSImage, types
from prefect import Flow, task

###############################################################################


@task
def select_cell_data(
    fov_path: types.PathLike,
    cell_id: int,
    cell_index: int
) -> da.Array:
    return


@task
def normalize_cell(cell_id: int, cell_data: da.Array) -> da.Array:
    return


@task
def create_normalized_cell_dataset(
    cell_ids: pd.Series,
    cell_indices: pd.Series,
    normalized_cells: List[da.Array]
) -> pd.DataFrame:
    return


@task
def project_cell(cell_id: int, normed_cell: da.Array) -> da.Array:
    return


@task
def create_cell_projection_dataset(
    cell_ids: pd.Series,
    cell_indices: pd.Series,
    cell_projections: List[da.Array]
) -> pd.DataFrame:
    return


@task
def downstream_analysis(normalized_cells: List[da.Array]) -> Any:
    return

###############################################################################

dataset = pd.DataFrame([
    {"fov_path": "/hello/world.ome.tiff", "cell_id": 1, "cell_index": 1},
    # {"fov_path": "/hello/world.ome.tiff", "cell_id": 2, "cell_index": 2},
    # {"fov_path": "/hello/world.ome.tiff", "cell_id": 3, "cell_index": 3},
])

with Flow("example_workflow") as flow:
    selected_cells = select_cell_data.map(
        list(dataset.fov_path),
        list(dataset.cell_id),
        list(dataset.cell_index),
    )

    normalized_cells = normalize_cell.map(
        list(dataset.cell_id),
        selected_cells,
    )

    normalized_cell_dataset = create_normalized_cell_dataset(
        list(dataset.cell_id),
        list(dataset.cell_index),
        normalized_cells,
        # some other metadata
    )

    cell_projections = project_cell.map(
        list(dataset.cell_id),
        normalized_cells,
    )

    cell_proj_dataset = create_cell_projection_dataset(
        list(dataset.cell_id),
        list(dataset.cell_index),
        cell_projections,
        # some other metadata
    )

    downstream_analysis(normalized_cells)

state = flow.run()
flow.visualize(flow_state=state, filename="static/flow", format="png")
