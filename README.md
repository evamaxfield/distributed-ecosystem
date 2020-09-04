# Pipeline and Distributed Ecosystem Tools and Planning
Planned tools for making pipeline development and data reproduction easier

## Goals

The goal of these tools is to allow the scientists to not focus on data storage or
parallel code distribution.

> Users should be able to run the same pipeline on their laptop with local or remote
> data, or on a distributed cluster with local or remote data* and the products of the
> pipeline should be tied to the code and be "publish ready".

-- Some scientist probably (it was Rory)

_* depending on the distributed cluster configuration, data must be local or remote but
usually cannot be both_

## Psuedo-code
The following is Python psuedo-code for the general end target for these tools.

It will shorten a common process known to many scientists in the institute:
1. selecting data you are interested in from an image
2. normalizing that data
3. storing projects or other representations of each selected datum


```python
from aicsimageio import AICSImage, types
import dask.array as da
from prefect import Flow, task

# A repo that currently doesn't exist
from databacked import (
    # Developer chooses which dataset level result they want
    LocalDatasetResult, QuiltDatasetResult, FMSDatasetResult,
    # Developer chooses which single item level result they want
    # LocalResult and S3Result are just routers to base prefect objects
    LocalResult, S3Result, FMSResult,
    # Various serializers for common data types we work with
    ArrayToOmeTiff, ArrayToDefaultWriter
)

###############################################################################

@task
def select_cell_data(fov_path: types.FSSpecLike, cell_index: int) -> da.Array:
    """
    Loads the image from any FSSpec like path and returns just the CZYX cell data.
    """
    img = AICSImage(fov_path)
    # ...
    return cell_data

@task(
    result=LocalResult(
        dir="local_staging/normalized_cells/",
        serializer=ArrayToOmeTiff(dimensions="CZYX", channel_names=["a", "b", "..."]),
    ),
    target=lambda **kwargs: "{}.ome.tiff".format(kwargs.get("cell_id")),
)
def normalize_cell(cell_id: int, cell_data: da.Array) -> da.Array:
    """
    Normalizes the array provided. Returns a dask array.

    The serializer object knows how to receive a dask array and return the bytes for an
    OME-TIFF.

    The result object knows to take the bytes and store them at some location for
    check-pointing / persistence.
    """
    # ...
    return normed_cell

@task(
    result=LocalResult(
        dir="local_staging/normalized_cells/",
        serializer=ArrayToDefaultWriter,
    ),
    target=lambda **kwargs: "{}.png".format(kwargs.get("cell_id")),
)
def project_cell(cell_id: int, normed_cell: da.Array) -> da.Array:
    """
    Max projects the array provided. Returns a dask array.

    The serializer object knows how to receive a dask array and return the bytes for a
    PNG.

    The result object knows to take the bytes and store them at some location for
    check-pointing / persistence.
    """
    # ... do some projection
    return projection

###############################################################################

# assume we have some dataset as a dataframe
# dataset = pd....

with Flow("example_workflow") as flow:
    selected_cells = select_cell_data.map(
        dataset.fov_path,
        dataset.cell_index,
    )

    normalized_cells = normalize_cell.map(
        dataset.cell_id,
        selected_cells,
    )

    cell_projections = project_cell.map(
        dataset.cell_id,
        normalized_cells
    )

flow.run()
```

### End Result of Pseudo-code

With current psuedo-code this results in:
1. Scientist doesn't have to care about file IO due to serializers
2. Results are _**checkpointed**_ at: `local_staging/` from current working directory
3. To move from local to remote they can find-replace `LocalResult` w/ `S3Result`*

_* I believe S3Result needs to be prefixed with s3://bucket-header, but still minimal
changes to move from local to remote_

#### Checkpointing

...

## Technology Choices

1. [AICSImageIO](#aicsimageio)
2. [Dask](#dask)
3. [Prefect](#prefect)


### AICSImageIO

...

### Dask

...

### Prefect

...


## The Last-Mile Library

"databacked" -- or whatever you want to name it.

1. "DatasetResult" Handlers
2. "ArrayTo*" Serializers

### DatasetResult Handlers

...

### ArrayTo Serializers

...
