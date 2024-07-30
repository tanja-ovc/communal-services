from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response


class ExceptionsHandlingMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if isinstance(exception, ObjectDoesNotExist):
            response = Response(
                data={'detail': f'Объект не найден: {exception}'},
                status=status.HTTP_404_NOT_FOUND
            )

        # elif isinstance(exception, IntegrityError):
        #     message: str = f'{exception}'
        #     logger.warning(f'{__name__}.{sys._getframe().f_code.co_name} - {message}')
        #
        #     if 'violates unique constraint' in message:
        #         response = Response(
        #             data={'detail': f'Такой объект уже существует: {exception}'},
        #             status=status.HTTP_406_NOT_ACCEPTABLE
        #         )
        #         return self._render_response(response, request)
        #
        #     elif 'violates foreign key constraint' in message:
        #         response = Response(
        #             data={'detail': f'Такого объекта для связи не существует: {exception}'},
        #             status=status.HTTP_404_NOT_FOUND
        #         )
        #         return self._render_response(response, request)
        #
        #     else:
        #         response = Response(
        #             data={'detail': message},
        #             status=status.HTTP_400_BAD_REQUEST
        #         )
        #         return self._render_response(response, request)
        #
        # elif isinstance(exception, ValueError):
        #     message: str = f'Неверное значение: {exception}'
        #     logger.warning(f'{__name__}.{sys._getframe().f_code.co_name} - {message}')
        #     response = Response(
        #         data={'detail': message},
        #         status=status.HTTP_422_UNPROCESSABLE_ENTITY
        #     )
        #     return self._render_response(response, request)
        else:
            response = Response(
                data={'detail': f'Ошибка при обработке запроса: {exception}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        return self._render_response(response, request)

    def _render_response(self, response, request):
        renderer = JSONRenderer()
        response.accepted_renderer = renderer
        response.accepted_media_type = renderer.media_type
        response.renderer_context = {
            'request': request,
            'response': response,
        }
        response.render()
        return response
