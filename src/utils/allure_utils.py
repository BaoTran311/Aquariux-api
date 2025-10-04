import hashlib
import json
import os
import re
from contextlib import suppress
from json import JSONDecodeError
from pathlib import Path

import allure

from src.core.response import XResponse
from src.data_runtime import DataRuntime
from src.utils.json_utils import truncate_json, extract_json_objects

line_spacing_info = "margin: 0 0 0.5em 0;"


def custom_log_info(_logmsgs):
    _logmsgs_checking = "verify check".split()
    if any(_msgs in _logmsgs.lower() for _msgs in _logmsgs_checking):
        result = f'<pre style="color:green;{line_spacing_info}">{_logmsgs}</pre>'
    else:
        match = re.search(r"(.*?)(\{.*\})", _tmplog := _logmsgs.replace(" ", "").replace("\n", "").replace("\t", ""), re.DOTALL)
        if match:
            method = match.group(1).strip()
            json_data = extract_json_objects(_tmplog)[-1]
            result = f"""
                <pre style="{line_spacing_info}">{method}{truncate_json(json.dumps(json.loads(json_data)))}</pre>
            """
        else:
            if any(x in _logmsgs.lower() for x in ("step", "steps")):
                result = f'<pre style="{line_spacing_info}"><b>{_logmsgs.strip()}</b></pre>'
            else:
                result = f'<pre style="{line_spacing_info}">{_logmsgs.strip()}</pre>'

    return result


def custom_log_warning(_logmsgs):
    if 'actual' in _logmsgs.lower():
        if re.findall(r"\{.*?\}", _tmplog := _logmsgs.replace(" ", "").replace("\n", "").replace("\t", ""), re.DOTALL):
            expect, actual = extract_json_objects(_tmplog)
            prefix_msg = re.split(r"\{", _logmsgs, 1)[0].strip()
            _logmsgs = f"""
                <pre style="color:red;{line_spacing_info}">{prefix_msg}{truncate_json(json.dumps(json.loads(expect)))}</pre>
            """
        else:
            if match := re.search(r'(\[Expected\][^\[]*)(?:\s*(\[Actual\].*))?', _logmsgs.replace("\n", "").replace("\t", ""), re.DOTALL):
                expect, actual = match.group(1) or "", match.group(2)
                prefix_msg = _logmsgs.split(expect.strip())[0].strip()
                _logmsgs = f'{prefix_msg} {"<br>" if expect else ("&nbsp;" * 5)}  {expect.strip()} {"&nbsp;" * 5} {actual.strip()}'
    return f"""
        <pre style="color:red;{line_spacing_info}">{_logmsgs.strip()}</pre>
    """


def delete_container_files(allure_dir):
    for container_file in Path(allure_dir).glob("*-container.json"):
        os.remove(container_file)


def attach_request_response(resp: XResponse, **kwargs):
    curl_cmd = resp.cash_request_to_curl().strip()
    try:
        response_json = json.dumps(resp.json(), indent=3)
    except JSONDecodeError:
        response_json = "Empty"

    body = f"""
            <div>

                <h3 style="margin: 0 0 5px 0; display: flex; justify-content: space-between; align-items: center;">
                    ➡️ Request Sent:
                </h3>

                <pre style="margin: 0; white-space: pre-wrap; word-wrap: break-word;
                                           resize: both; overflow: auto;">{curl_cmd}</pre>

                <h3 style="margin: 12px 0 5px 0; display: flex; justify-content: space-between; align-items: center;">
                    ⬅️ Response Received:
                </h3>

                <pre style="margin: 0; white-space: pre-wrap; word-wrap: break-word;
                                            resize: both; overflow: auto;">{response_json}</pre>
            </div>
            """
    name = f"{kwargs.get("request_time")} | [{resp.request.method}] {resp.request.path_url}"
    if kwargs.get("html"):
        allure.attach(
            body,
            name=name,
            attachment_type=allure.attachment_type.HTML
        )
        return

    allure.attach(
        name=name,
        body=format_request_response(resp).strip(),
    )


def format_request_response(resp: XResponse):
    req = f"\n➡️  Request Sent:\n{resp.cash_request_to_curl().strip()}"
    try:
        resp = f"⬅️  Response Received:\n{json.dumps(resp.json(), indent=3).strip()}"
    except JSONDecodeError:
        resp = f"⬅️  Response Received: Empty"

    return f"{req}{'\n' * 2}{resp}"


def __generate_history_id__(full_name: str, parameters):
    """Generate Allure historyId based on result.json content."""
    # Check if test case contains parameters
    if isinstance(parameters, list) and parameters:
        params_str = ''.join(f"{p.get('name')}={p.get('value')}" for p in parameters)
    else:
        params_str = ""

    # Generate hash md5
    raw = f"{full_name}{params_str}{DataRuntime.option.client}{DataRuntime.option.server}"
    return hashlib.md5(raw.encode("utf-8")).hexdigest()


def custom_allure_result(allure_dir):
    for result_file in Path(allure_dir).glob("*-result.json"):
        with result_file.open("r", encoding="utf8") as _rf:
            # Avoid error json file from allure generate
            with suppress(JSONDecodeError):
                json_obj = json.load(_rf)

                json_obj['historyId'] = __generate_history_id__(json_obj['fullName'], json_obj.get('parameters'))

                # Remove unnecessary labels
                raw_labels = json_obj.get("labels", [])
                json_obj["labels"] = [
                    _label for _label in raw_labels
                    if _label.get('name') in ("parentSuite", "suite", "tag")
                ]

                # Write the modified json object
                with result_file.open("w") as _f:
                    json.dump(json_obj, _f)
