import os

import pandas as pd

from cl_search.database import create_session
from cl_search.database import query_post_id
from cl_search.database import setup_database
from cl_search.utils import get_city_name
from cl_search.utils import get_current_time
from cl_search.utils import project_path


def get_export_formats(df=pd.DataFrame) -> dict:
    try:
        # import jinja2
        # from astropy.table import Table

        jinja_available = True
    except ImportError:
        jinja_available = False

    export_formats_dict = {
        # write, extension, read
        "csv": (df.to_csv, "csv", pd.read_csv),
        "json": (df.to_json, "json", pd.read_json),
        # "html": (df.to_html, "html", pd.read_html),
        # "xml": (df.to_xml, "xml", pd.read_xml),
        # "excel": (df.to_excel, "xlsx", pd.read_excel),  # requires openpyxl
        # "xlsx": (df.to_excel, "xlsx", pd.read_excel),
        # "hdf5": (df.to_hdf, "h5", pd.read_hdf),
        # "hdf": (df.to_hdf, "h5", pd.read_hdf),
        # "h5": (df.to_hdf, "h5", pd.read_hdf),
        # "feather": (df.to_feather, "feather", pd.read_feather),
        # "parquet": (df.to_parquet, "parquet", pd.read_parquet),
        # "orc": (df.to_orc, "orc", pd.read_orc),
        # "stata": (df.to_stata, "dta", pd.read_stata),
        # "dta": (df.to_stata, "dta", pd.read_stata),
        # "pickle": (df.to_pickle, "pkl", pd.read_pickle),
        # "pkl": (df.to_pickle, "pkl", pd.read_pickle),
        "sql": (df.to_sql, "db", pd.read_sql),
        "sqlite": (df.to_sql, "db", pd.read_sql),
        "db": (df.to_sql, "db", pd.read_sql),
        # "clipboard": (df.to_clipboard, "clip", pd.read_clipboard),
    }

    if jinja_available is True:
        # s = df.style  # requires jinja2
        export_formats_dict.update(
            {  # reading requires astropy
                # "latex": (lambda: s.to_latex(), "tex", lambda: Table.read().to_pandas()),
                # "tex": (lambda: s.to_latex(), "tex", lambda: Table.read().to_pandas()),
            }
        )

    return export_formats_dict


def get_default_options() -> dict:

    default_options_dict = {
        # write, append, read
        "csv": (
            {"mode": "w", "index": False, "header": True},
            {"mode": "a", "index": False, "header": False},
            {}
        ),
        "json": (
            {"mode": "w", "index": False, "orient": 'records', 'lines': True},
            {"mode": "a", "index": False, "orient": 'records', 'lines': True},
            {"orient": 'records', 'lines': True}
        ),
        "html": (
            {"index": False, "header": True},
            {"index": False, "header": False},
            {}
        ),
        "xml": (
            {"index": False},
            {"index": False},
            {}
        ),
        "excel": (
            {"index": False, "header": True},
            {"index": False, "header": True},
            {"engine": "openpyxl"}
        ),
        "excel_writer": (
            {"mode": "w", "engine": "openpyxl"},
            {"mode": "a", "if_sheet_exists": 'overlay', "engine": "openpyxl"},
            {}
        ),
        "sql": (
            {},
            {},
            {}
        )
    }

    return default_options_dict


def df_output(city_name: str, df: pd.DataFrame, options: dict = None, **kwargs) -> None:
    # driver_options = kwargs.get("driver_options", None)
    output = kwargs.get("output", "csv").lower()
    location = kwargs.get("location")
    file_extension = kwargs.get("file_extension")
    search_query = kwargs.get("search_query", None).lower()

    source_name = f"craigslist_{city_name}"
    default_options = get_default_options()
    export_formats = get_export_formats(df)

    # remove sheet dir
    # implement custom driver_options

    sheets = f"{project_path}/sheets"

    if not os.path.exists(sheets):
        os.makedirs(sheets)

    if output in export_formats:
        function_name, file_extension, file_read = export_formats[output]

    if output in default_options:
        write_options, append_options, read_options = default_options[output]

    if options is None:
        options = append_options
        # if driver_options is None:
        #     options = append_options
        # else:
        #     options = driver_options

    if function_name:
        output_file = f"{sheets}/{location}_{search_query}.{file_extension}"

        if output == "clipboard":
            df.to_clipboard()
            print("Ready to paste")

        elif output == 'sql':
            if os.path.isfile(f'{project_path}/craigslist.db') is False:
                db = setup_database()
                query_post_id(db, df, **kwargs)

            else:
                session = create_session()
                query_post_id(session, df, **kwargs)
                session.commit()

        elif output == 'excel':
            # fix excel not appending properly
            excel_writer_write, excel_writer_append, excel_writer_read = default_options[
                "excel_writer"]

            if not os.path.isfile(output_file):
                with pd.ExcelWriter(output_file, **excel_writer_write) as writer:
                    function_name(writer, **options, sheet_name=source_name)

            else:
                with pd.ExcelWriter(output_file, **excel_writer_append) as writer:
                    function_name(writer, **options, sheet_name=source_name)

        else:
            function_name(output_file, **options)

    else:
        print(f"Invalid output format or extension: {options}.")


def write_frames(link: str, craigslist_posts: list, options: dict = None, **kwargs) -> None:
    city_name = get_city_name(link)
    source_name = f"craigslist_{city_name}"
    current_time = get_current_time()

    df = pd.DataFrame([x.as_dict() for x in craigslist_posts])

    df.insert(0, "last_updated", current_time)
    df.insert(0, "time_added", current_time)
    df.insert(0, "is_new", 1)
    df.insert(0, "source", f"{source_name}")

    df.dropna(inplace=True)
    df_output(city_name, df, options, **kwargs)
