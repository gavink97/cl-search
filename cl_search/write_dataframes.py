import os

import pandas as pd

from cl_search.utils import get_current_time
from cl_search.utils import parse_url
from cl_search.utils import project_path


def get_export_formats(df=pd.DataFrame) -> dict:
    try:
        import jinja2

        jinja_available = True
    except ImportError:
        jinja_available = False

    export_formats_dict = {
        "csv": (df.to_csv, "csv"),
        "json": (df.to_json, "json"),
        "html": (df.to_html, "html"),
        "xml": (df.to_xml, "xml"),
        "excel": (df.to_excel, "xlsx"),
        "xlsx": (df.to_excel, "xlsx"),
        "hdf5": (df.to_hdf, "h5"),
        "hdf": (df.to_hdf, "h5"),
        "h5": (df.to_hdf, "h5"),
        "feather": (df.to_feather, "feather"),
        "parquet": (df.to_parquet, "parquet"),
        "orc": (df.to_orc, "orc"),
        "stata": (df.to_stata, "dta"),
        "dta": (df.to_stata, "dta"),
        "pickle": (df.to_pickle, "pkl"),
        "pkl": (df.to_pickle, "pkl"),
    }

    if jinja_available is True:
        s = df.style  # requires jinja2
        export_formats_dict.update(
            {
                "latex": (lambda: s.to_latex(), "tex"),
                "tex": (lambda: s.to_latex(), "tex"),
            }
        )

    return export_formats_dict


def df_output(city_name: str, df=pd.DataFrame, output_arg: str = "csv") -> None:
    # add 'sql' support
    # add 'gbq' support
    # add options for formats

    export_formats = get_export_formats(df)
    sheets = f"{project_path}/sheets"
    source_name = f"craigslist_{city_name}"

    if not os.path.exists(sheets):
        os.makedirs(sheets)

    if output_arg in export_formats:
        function_name, file_extension = export_formats[output_arg]

    if function_name:
        output_file = f"{sheets}/{source_name}.{file_extension}"

        function_name(output_file)
        print(f"Created {source_name}.{file_extension}")

    elif output_arg == "clipboard":
        df.to_clipboard()
        print("Ready to paste")

    else:
        print(f"Invalid output format or extension: {output_arg}.")


def write_frames(link: str, craigslist_posts: list, output_arg: str = "csv") -> None:
    city_name = parse_url(link)
    current_time = get_current_time()
    source_name = f"craigslist_{city_name}"

    df = pd.DataFrame([x.as_dict() for x in craigslist_posts])
    df.insert(0, "time_added", current_time)
    df.insert(0, "is_new", "1")
    df.insert(0, "source", f"{source_name}")

    if "post_id" in df.columns:
        df.set_index("post_id", inplace=True)

    df.dropna(inplace=True)
    df_output(city_name, df, output_arg)
