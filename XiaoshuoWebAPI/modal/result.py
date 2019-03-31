from django.http import JsonResponse


class HttpCode(object):
    success = 200  # 成功
    error = 403  # 失败


def result(code=HttpCode.success, message='', data=None):
    res_json = {'code': code, 'message': message, 'data': data}
    return JsonResponse(res_json, json_dumps_params={'ensure_ascii': False})


def success(data=None):
    return result(code=HttpCode.success, message='成功', data=data)


def error(message='', data=None):
    return result(code=HttpCode.error, message=message, data=data)
