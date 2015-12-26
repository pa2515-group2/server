from __future__ import absolute_import#, division, print_function

from wsgiref import simple_server
import json
import sys, os
import datetime
import functools

import falcon

from server import doctor, patient, appointment, obj
from server.utils import logger


def max_body(limit):

    def hook(req, resp, resource, params):
        length = req.content_length
        if length is not None and length > limit:
            msg = ('The size of the request is too large. The body must not '
                   'exceed ' + str(limit) + ' bytes in length.')

            raise falcon.HTTPRequestEntityTooLarge(
                'Request body is too large', msg)
    return hook


class RegDoctorListener:

    @falcon.before(max_body(64*1024))
    def on_post(self, req, resp):
        """
        Register a doctor in the system. The post data is in json format.

        :param req.header.username: username
        :param req.header.password: password
        :returns: a json contains doctor's id, or other related info
                {"doctorid":'d001', "info":{"info1":''}}
        """
        resp_dict = {}
        try:
            username = req.get_header('username') or 'un'
            password = req.get_header('password') or 'pw'
            # post_data = req.params.get('data')
            # have pre-processed by JSONTranslator, post_data is a dict
            post_data = req.context['doc']
            # logger.debug('username:%s, password:%s, data:%s'
            #     % (username, password, post_data))
            # logger.debug('env:%s , \nstream:%s, \ncontext:, \ninput:' % (
            #     req.env, req.stream.read()))
        except Exception as ex:
            logger.error('error when try to get headers and data, ', ex)
            raise falcon.HTTPBadRequest('bad req',
                'when read from req, please check if the req is correct.')
        try:
            """
            handle_request:

            """
            status, doctorid = doctor.register_doctor(post_data)

        except Exception as ex:
            logger.exception('error when register doctor, ', ex)
            resp_dict['info'] = 'Error when register doctor {}'.format(
                post_data['lastname'])
            resp.status = falcon.HTTP_500
            resp.body = json.dumps(resp_dict, sort_keys=True, indent=4)
        else:
            if status:
                logger.debug('register ok, status positive')
                resp_dict['info'] = 'Register doctor {} success'.format(
                    post_data['lastname'])
                resp_dict['doctorid'] = doctorid
                # resp.status = status or falcon.HTTP_200
                resp.status = falcon.HTTP_201
                resp.body = json.dumps(resp_dict)
            else:
                logger.exception('return error when try to register doctor, ', ex)
                resp_dict['errinfo'] = 'Error when register doctor {}'.format(
                    post_data['lastname'])
                resp.status = falcon.HTTP_400
                resp.body = json.dumps(resp_dict)

class DoctorListener:

    def on_get(self, req, resp, doctorid):
        """
        Get info of a doctor in the system. The response data is in json format.

        :param req.header.username: username
        :param req.header.password: password
        :returns: a json contains doctor's info
                {"doctorid":'d001', "info":{"info1":''}}
        """
        resp_dict = {}
        try:
            username = req.get_header('username') or 'un'
            password = req.get_header('password') or 'pw'
            # logger.debug('env:%s , \nstream:%s, \ncontext:, \ninput:' % (
            #     req.env, req.stream.read()))
        except Exception as ex:
            logger.error('error when try to get headers and data, ', ex)
            raise falcon.HTTPBadRequest('bad req',
                'when read from req, please check if the req is correct.')
        try:
            """
            handle_request:

            """
            status, doctorinfo = doctor.get_doctor(doctorid)

        except Exception as ex:
            logger.exception('error when get doctor, ', ex)
            resp_dict['info'] = 'Error when get doctor {}'.format(
                doctorid)
            resp.status = falcon.HTTP_500
            resp.body = json.dumps(resp_dict, sort_keys=True, indent=4)
        else:
            if status:
                logger.debug('get ok, status positive')
                resp_dict['info'] = 'Get doctor {} success'.format(
                    doctorid)
                resp_dict['doctorinfo'] = doctorinfo
                # resp.status = status or falcon.HTTP_200
                resp.status = falcon.HTTP_200
                resp.body = json.dumps(resp_dict)
            else:
                logger.exception('return error when try to get doctor')
                resp_dict['info'] = 'Error when get doctor {}'.format(
                    doctorid)
                resp.status = falcon.HTTP_400
                resp.body = json.dumps(resp_dict)

    @falcon.before(max_body(64*1024))
    def on_put(self, req, resp, doctorid):
        """
        Edit a doctor in the system. The PUT data is in json format.

        :param req.header.username: username
        :param req.header.password: password
        :returns: a json contains doctor's id, or other related info
                {"doctorid":'d001', "info":{"info1":''}}
        """
        resp_dict = {}
        logger.debug('in doctor put')

        try:
            username = req.get_header('username') or 'un'
            password = req.get_header('password') or 'pw'
            # post_data = req.params.get('data')
            # have pre-processed by JSONTranslator, post_data is a dict
            logger.debug('in doctor put, before got post_data')

            post_data = req.context['doc']
            # logger.debug('username:%s, password:%s, data:%s'
            #     % (username, password, post_data))
            # logger.debug('env:%s , \nstream:%s, \ncontext:, \ninput:' % (
            #     req.env, req.stream.read()))
        except Exception as ex:
            logger.error('error when try to get headers and data, ', ex)
            raise falcon.HTTPBadRequest('bad req',
                'when read from req, please check if the req is correct.')
        try:
            """
            handle_request:

            """
            status, doctorid = doctor.edit_doctor(doctorid, post_data)

        except Exception as ex:
            logger.exception('error when register doctor, ', ex)
            resp_dict['info'] = 'Error when register doctor {}'.format(
                doctorid)
            resp.status = falcon.HTTP_500
            resp.body = json.dumps(resp_dict, sort_keys=True, indent=4)
        else:
            if status:
                logger.debug('Edit ok, status positive')
                resp_dict['info'] = 'Edit doctor {} success'.format(
                    doctorid)
                resp_dict['doctorid'] = doctorid
                # resp.status = status or falcon.HTTP_200
                resp.status = falcon.HTTP_200
                resp.body = json.dumps(resp_dict)
            else:
                logger.exception('return error when try to Edit doctor, ', ex)
                resp_dict['errinfo'] = 'Error when Edit doctor {}'.format(
                    doctorid)
                resp.status = falcon.HTTP_400
                resp.body = json.dumps(resp_dict)

    def on_delete(self, req, resp):
        pass


class RegPatientListener:

    @falcon.before(max_body(64*1024))
    def on_post(self, req, resp):
        """
        Register a doctor in the system. The post data is in json format.

        :param req.header.username: username
        :param req.header.password: password
        :returns: a json contains patient's id, or other related info
                {"patientid":'d001', "info":{"info1":''}}
        """
        resp_dict = {}
        try:
            username = req.get_header('username') or 'un'
            password = req.get_header('password') or 'pw'
            # post_data = req.params.get('data')
            # have pre-processed by JSONTranslator, post_data is a dict
            post_data = req.context['doc']
            # logger.debug('username:%s, password:%s, data:%s'
            #     % (username, password, post_data))
            # logger.debug('env:%s , \nstream:%s, \ncontext:, \ninput:' % (
            #     req.env, req.stream.read()))
        except Exception as ex:
            logger.error('error when try to get headers and data, ', ex)
            raise falcon.HTTPBadRequest('bad req',
                'when read from req, please check if the req is correct.')
        try:
            """
            handle_request:

            """
            status, patientid = patient.register_patient(post_data)

        except Exception as ex:
            logger.exception('error when register patient, ', ex)
            resp_dict['info'] = 'Error when register patient {}'.format(
                post_data['lastname'])
            resp.status = falcon.HTTP_500
            resp.body = json.dumps(resp_dict, sort_keys=True, indent=4)
        else:
            if status:
                logger.debug('register ok, status positive')
                resp_dict['info'] = 'Register patient {} success'.format(
                    post_data['lastname'])
                resp_dict['patientid'] = patientid
                # resp.status = status or falcon.HTTP_200
                resp.status = falcon.HTTP_201
                resp.body = json.dumps(resp_dict)
            else:
                logger.exception('return error when try to register patient, ', ex)
                resp_dict['errinfo'] = 'Error when register patient {}'.format(
                    post_data['lastname'])
                resp.status = falcon.HTTP_400
                resp.body = json.dumps(resp_dict)
                # resp.body = json.dumps(resp_dict, sort_keys=True,
                #     indent=4)


class PatientListener:

    def on_get(self, req, resp, patientid):
        """
        Get info of a patient in the system. The response data is in json format.

        :param req.header.username: username
        :param req.header.password: password
        :returns: a json contains doctor's info
                {"patientid":'d001', "info":{"info1":''}}
        """
        resp_dict = {}
        try:
            username = req.get_header('username') or 'un'
            password = req.get_header('password') or 'pw'
            # logger.debug('env:%s , \nstream:%s, \ncontext:, \ninput:' % (
            #     req.env, req.stream.read()))
        except Exception as ex:
            logger.error('error when try to get headers and data, ', ex)
            raise falcon.HTTPBadRequest('bad req',
                'when read from req, please check if the req is correct.')
        try:
            """
            handle_request:

            """
            status, patientinfo = patient.get_patient(patientid)

        except Exception as ex:
            logger.exception('error when get patient, ', ex)
            resp_dict['info'] = 'Error when get patient {}'.format(
                patientid)
            resp.status = falcon.HTTP_500
            resp.body = json.dumps(resp_dict, sort_keys=True, indent=4)
        else:
            if status:
                logger.debug('get ok, status positive')
                resp_dict['info'] = 'Get patient {} success'.format(
                    patientid)
                resp_dict['patientinfo'] = patientinfo
                # resp.status = status or falcon.HTTP_200
                resp.status = falcon.HTTP_200
                resp.body = json.dumps(resp_dict)
            else:
                logger.exception('return error when try to get patient')
                resp_dict['info'] = 'Error when get patient {}'.format(
                    patientid)
                resp.status = falcon.HTTP_400
                resp.body = json.dumps(resp_dict)

    @falcon.before(max_body(64*1024))
    def on_put(self, req, resp, patientid):
        """
        Edit a patient in the system. The PUT data is in json format.

        :param req.header.username: username
        :param req.header.password: password
        :returns: a json contains patient's id, or other related info
                {"patientid":'d001', "info":{"info1":''}}
        """
        resp_dict = {}
        logger.debug('in patient put')

        try:
            username = req.get_header('username') or 'un'
            password = req.get_header('password') or 'pw'
            # post_data = req.params.get('data')
            # have pre-processed by JSONTranslator, post_data is a dict
            logger.debug('in patient put, before got post_data')

            post_data = req.context['doc']
            # logger.debug('username:%s, password:%s, data:%s'
            #     % (username, password, post_data))
            # logger.debug('env:%s , \nstream:%s, \ncontext:, \ninput:' % (
            #     req.env, req.stream.read()))
        except Exception as ex:
            logger.error('error when try to get headers and data, ', ex)
            raise falcon.HTTPBadRequest('bad req',
                'when read from req, please check if the req is correct.')
        try:
            """
            handle_request:

            """
            status, patientid = patient.edit_patient(patientid, post_data)

        except Exception as ex:
            logger.exception('error when register patient, ', ex)
            resp_dict['info'] = 'Error when register patient {}'.format(
                patientid)
            resp.status = falcon.HTTP_500
            resp.body = json.dumps(resp_dict, sort_keys=True, indent=4)
        else:
            if status:
                logger.debug('Edit ok, status positive')
                resp_dict['info'] = 'Edit patient {} success'.format(
                    patientid)
                resp_dict['patientid'] = patientid
                # resp.status = status or falcon.HTTP_200
                resp.status = falcon.HTTP_200
                resp.body = json.dumps(resp_dict)
            else:
                logger.exception('return error when try to Edit patient, ', ex)
                resp_dict['errinfo'] = 'Error when Edit patient {}'.format(
                    patientid)
                resp.status = falcon.HTTP_400
                resp.body = json.dumps(resp_dict)

    def on_delete(self, req, resp):
        pass


class MakeAppointmentListener:

    @falcon.before(max_body(64*1024))
    def on_post(self, req, resp):
        """
        Make an appointment in the system. The post data is in json format.

        :param req.header.username: username
        :param req.header.password: password
        :returns: a json contains the appointment's url, or other related info
        """
        resp_dict = {}
        try:
            username = req.get_header('username') or 'un'
            password = req.get_header('password') or 'pw'
            # post_data = req.params.get('data')
            # have pre-processed by JSONTranslator, post_data is a dict
            post_data = req.context['doc']
            # logger.debug('username:%s, password:%s, data:%s'
            #     % (username, password, post_data))
            # logger.debug('env:%s , \nstream:%s, \ncontext:, \ninput:' % (
            #     req.env, req.stream.read()))
        except Exception as ex:
            logger.error('error when try to get headers and data, ', ex)
            raise falcon.HTTPBadRequest('bad req',
                'when read from req, please check if the req is correct.')
        try:
            status, appointment_url = appointment.make_appointment(post_data)

        except Exception as ex:
            logger.exception('error when Make an appointment, ', ex)
            resp_dict['info'] = 'Error when Make an appointment {}'.format(
                post_data['doctorid']+post_data['patientid']+post_data['datetimeslot'])
            resp.status = falcon.HTTP_500
            resp.body = json.dumps(resp_dict, sort_keys=True, indent=4)
        else:
            if status:
                logger.debug('make appointment ok, status positive')
                resp_dict['info'] = 'make appointment {} success'.format(
                    post_data['doctorid']+post_data['patientid']+post_data['datetimeslot'])
                resp_dict['appointment_url'] = appointment_url
                # resp.status = status or falcon.HTTP_200
                resp.status = falcon.HTTP_201
                resp.body = json.dumps(resp_dict,
                    sort_keys=True, indent=4)
            else:
                logger.error('return error when try to make appointment')
                resp_dict['errinfo'] = 'Error when make appointment {}'.format(
                    post_data['doctorid']+post_data['patientid']+post_data['datetimeslot'])
                resp.status = falcon.HTTP_400
                resp.body = json.dumps(resp_dict)


class AppointmentListener:


    def on_get(self, req, resp, doctorid, datetimeslot, patientid):
        """
        Get info of a doctor in the system. The response data is in json format.

        :param req.header.username: username
        :param req.header.password: password
        :returns: a json contains doctor's info
                {"doctorid":'d001', "info":{"info1":''}}
        """
        resp_dict = {}
        try:
            username = req.get_header('username') or 'un'
            password = req.get_header('password') or 'pw'
            # logger.debug('env:%s , \nstream:%s, \ncontext:, \ninput:' % (
            #     req.env, req.stream.read()))
        except Exception as ex:
            logger.error('error when try to get headers and data, ', ex)
            raise falcon.HTTPBadRequest('bad req',
                'when read from req, please check if the req is correct.')
        try:
            """
            handle_request:

            """
            apmt_url = doctorid + '/' + datetimeslot + '/' + patientid
            status, appointment_info = appointment.get_appointment(apmt_url)

        except Exception as ex:
            logger.exception('error when get appointment_info, ', ex)
            resp_dict['info'] = 'Error when get appointment_info {}'.format(
                apmt_url)
            resp.status = falcon.HTTP_500
            resp.body = json.dumps(resp_dict, sort_keys=True, indent=4)
        else:
            if status:
                logger.debug('get ok, status positive')
                resp_dict['info'] = 'Get appointment_info {} success'.format(
                    apmt_url)
                resp_dict['appointment_info'] = appointment_info
                # resp.status = status or falcon.HTTP_200
                resp.status = falcon.HTTP_200
                resp.body = json.dumps(resp_dict,
                    sort_keys=True, indent=4)
            else:
                logger.exception('return error when try to get appointment_info')
                resp_dict['info'] = 'Error when get appointment_info {}'.format(
                    apmt_url)
                resp.status = falcon.HTTP_400
                resp.body = json.dumps(resp_dict, sort_keys=True,
                    indent=4)

    def on_put(self, req, resp):
        pass

    def on_delete(self, req, resp):
        pass



class AppointmentListListener:


    def on_get(self, req, resp, doctorid, date):
        """
        Get info of a doctor in the system. The response data is in json format.

        :param req.header.username: username
        :param req.header.password: password
        :returns: a json contains doctor's info
                {"doctorid":'d001', "info":{"info1":''}}
        """
        resp_dict = {}
        try:
            username = req.get_header('username') or 'un'
            password = req.get_header('password') or 'pw'
            # logger.debug('env:%s , \nstream:%s, \ncontext:, \ninput:' % (
            #     req.env, req.stream.read()))
        except Exception as ex:
            logger.error('error when try to get headers and data, ', ex)
            raise falcon.HTTPBadRequest('bad req',
                'when read from req, please check if the req is correct.')
        try:
            """
            handle_request:

            """
            status, appointment_info = appointment.check_appointment(doctorid, date)

        except Exception as ex:
            logger.exception('error when get appointment_info, ', ex)
            resp_dict['info'] = 'Error when get appointment_info {}'.format(
                apmt_url)
            resp.status = falcon.HTTP_500
            resp.body = json.dumps(resp_dict, sort_keys=True, indent=4)
        else:
            if status:
                logger.debug('get ok, status positive')
                resp_dict['info'] = 'Get appointment_info {} success'.format(
                    apmt_url)
                resp_dict['appointment_info'] = appointment_info
                # resp.status = status or falcon.HTTP_200
                resp.status = falcon.HTTP_200
                resp.body = json.dumps(resp_dict,
                    sort_keys=True, indent=4)
            else:
                logger.exception('return error when try to get appointment_info')
                resp_dict['info'] = 'Error when get appointment_info {}'.format(
                    apmt_url)
                resp.status = falcon.HTTP_400
                resp.body = json.dumps(resp_dict, sort_keys=True,
                    indent=4)

    def on_put(self, req, resp):
        pass

    def on_delete(self, req, resp):
        pass


class AppointmentSinkAdapter(object):
    def __call__(self, req, resp, doctor_date):
        """
        :param req.header.username: the username, should be tenant:user when dev
        :param req.header.password: password
        :doctor_date the part in the request url /v1/disk/(?P<doctor_date>.+?), to
            identify the resource to manipulate

        :returns: a json contains correspond response info
            GET: the temp_url of the file in a resp dict
            PUT: the auth_token and storage_url in a resp dict for uploading file
            DELETE: description of if the operation success or fail
        """
        logger.debug('in sink req.method:%s  doctor_date:%s' % (
            req.method, doctor_date))
        resp_dict = {}

        try:
            username = req.get_header('username') or 'un'
            password = req.get_header('password') or 'pw'
            req_dir = req.get_header('dir') or None
            logger.debug('username:%s, password:%s' % (username, password))
        except:
            raise falcon.HTTPBadRequest('bad req',
                'when read from req, please check if the req is correct.')

        if req.method == 'GET':
            try:
                url_list = doctor_date.split('/')
                if len(url_list) == 2:
                    # check_appointment
                    logger.debug(url_list)
                    status, schedule = appointment.check_appointment(url_list[0], url_list[1])
                    logger.debug('in sink schedule data:{}'.format(schedule))

            # except UserNotExistException:
                # logger.debug('in UserNotExistException')
                # resp_dict['info'] = 'user:%s does not exist' % username
                # resp.status = falcon.HTTP_404
                # resp.body = json.dumps(resp_dict, encoding='utf-8')

            except:
                description = ('Unknown error, username and passwd ok!')
                raise falcon.HTTPServiceUnavailable(
                        'Service Error',
                        description,
                        30)
            else:
                # resp_dict['info'] = 'doctor_date:%s ' % doctor_date

                if status:
                    logger.debug('get ok, status positive')
                    resp.status = falcon.HTTP_200
                    resp.body = schedule
                else:
                    logger.exception('return error when try to get appointment_info')
                    resp_dict['info'] = 'Error when get appointment_info {}'.format(
                        apmt_url)
                    resp.status = falcon.HTTP_400
                    resp.body = json.dumps(resp_dict, sort_keys=True,
                        indent=4)



class PostObjListener:

    # @falcon.before(max_body(64*1024))
    def on_post(self, req, resp, patientid):
        """
        Register a doctor in the system. The post data is in json format.

        :param req.header.username: username
        :param req.header.password: password
        :returns: a json contains patient's id, or other related info
                {"patientid":'d001', "info":{"info1":''}}
        """
        resp_dict = {}
        try:
            username = req.get_header('username') or 'un'
            password = req.get_header('password') or 'pw'
            # post_data = req.params.get('data')
            # have pre-processed by JSONTranslator, post_data is a dict
            post_data = req.context['doc']
            # logger.debug('username:%s, password:%s, data:%s'
            #     % (username, password, post_data))
            # logger.debug('env:%s , \nstream:%s, \ncontext:, \ninput:' % (
            #     req.env, req.stream.read()))
        except Exception as ex:
            logger.error('error when try to get headers and data, ', ex)
            raise falcon.HTTPBadRequest('bad req',
                'when read from req, please check if the req is correct.')
        try:
            """
            handle_request:

            """
            status, obj_dict = obj.upload_obj(patientid, post_data)

        except Exception as ex:
            logger.exception('error when register patient, ', ex)
            resp_dict['info'] = 'Error when register patient {}'.format(
                'obj')
            resp.status = falcon.HTTP_500
            resp.body = json.dumps(resp_dict, sort_keys=True, indent=4)
        else:
            if status:
                logger.debug('register ok, status positive')
                # resp_dict['info'] = 'Register patient {} success'.format(
                #     'obj')
                # resp_dict['objid'] = objid
                # resp.status = status or falcon.HTTP_200
                resp.status = falcon.HTTP_201
                resp.body = json.dumps(obj_dict)
            else:
                logger.exception('return error when try to register patient, ', ex)
                resp_dict['errinfo'] = 'Error when register patient {}'.format(
                    'obj')
                resp.status = falcon.HTTP_400
                resp.body = json.dumps(resp_dict)
                # resp.body = json.dumps(resp_dict, sort_keys=True,
                #     indent=4)


class ObjectListener:

    def on_get(self, req, resp, patientid, objid):
        """
        Get info of a patient in the system. The response data is in json format.

        :param req.header.username: username
        :param req.header.password: password
        :returns: a json contains doctor's info
                {"objid":'d001', "info":{"info1":''}}
        """
        resp_dict = {}
        try:
            username = req.get_header('username') or 'un'
            password = req.get_header('password') or 'pw'
            # logger.debug('env:%s , \nstream:%s, \ncontext:, \ninput:' % (
            #     req.env, req.stream.read()))
        except Exception as ex:
            logger.error('error when try to get headers and data, ', ex)
            raise falcon.HTTPBadRequest('bad req',
                'when read from req, please check if the req is correct.')
        try:
            """
            handle_request:

            """
            status, obj_dict = obj.get_obj(patientid, objid)

        except Exception as ex:
            logger.exception('error when get object, ', ex)
            resp_dict['errinfo'] = 'Error when get patietn:{} object {}'.format(
                patientid, objid)
            resp.status = falcon.HTTP_500
            resp.body = json.dumps(resp_dict, sort_keys=True, indent=4)
        else:
            if status:
                logger.debug('get ok, status positive')
                # resp_dict['info'] = 'Register patient {} success'.format(
                #     'obj')
                # resp_dict['objid'] = objid
                # resp.status = status or falcon.HTTP_200
                resp.status = falcon.HTTP_200
                resp.body = json.dumps(obj_dict)
            else:
                logger.exception('return error when try to get object, ', ex)
                resp_dict['errinfo'] = 'Error when get patietn:{} object {}'.format(
                    patientid, objid)
                resp.status = falcon.HTTP_400
                resp.body = json.dumps(resp_dict)
                # resp.body = json.dumps(resp_dict, sort_keys=True,
                #     indent=4)

    def on_delete(self, req, resp, patientid, objid):
        """
        Get info of a patient in the system. The response data is in json format.

        :param req.header.username: username
        :param req.header.password: password
        :returns: a json contains doctor's info
                {"objid":'d001', "info":{"info1":''}}
        """
        resp_dict = {}
        try:
            username = req.get_header('username') or 'un'
            password = req.get_header('password') or 'pw'
            # logger.debug('env:%s , \nstream:%s, \ncontext:, \ninput:' % (
            #     req.env, req.stream.read()))
        except Exception as ex:
            logger.error('error when try to get headers and data, ', ex)
            raise falcon.HTTPBadRequest('bad req',
                'when read from req, please check if the req is correct.')
        try:
            """
            handle_request:

            """
            status, obj_dict = obj.delete_obj(patientid, objid)

        except Exception as ex:
            logger.exception('error when delete object, ', ex)
            resp_dict['errinfo'] = 'Error when delete patietn:{} object {}'.format(
                patientid, objid)
            resp.status = falcon.HTTP_500
            resp.body = json.dumps(resp_dict, sort_keys=True, indent=4)
        else:
            if status:
                logger.debug('delete ok, status positive')
                # resp_dict['info'] = 'Register patient {} success'.format(
                #     'obj')
                # resp_dict['objid'] = objid
                # resp.status = status or falcon.HTTP_200
                resp.status = falcon.HTTP_204
                resp.body = json.dumps(obj_dict)
            else:
                logger.exception('return error when try to delete object, ', ex)
                resp_dict['errinfo'] = 'Error when delete patietn:{} object {}'.format(
                    patientid, objid)
                resp.status = falcon.HTTP_400
                resp.body = json.dumps(resp_dict)
                # resp.body = json.dumps(resp_dict, sort_keys=True,
                #     indent=4)


class ObjectListListener:

    def on_get(self, req, resp, patientid):
        """
        Get info of a patient in the system. The response data is in json format.

        :param req.header.username: username
        :param req.header.password: password
        :returns: a json contains doctor's info
                {"patientid":'d001', "info":{"info1":''}}
        """
        resp_dict = {}
        try:
            username = req.get_header('username') or 'un'
            password = req.get_header('password') or 'pw'
            # post_data = req.params.get('data')
            # have pre-processed by JSONTranslator, post_data is a dict
            # post_data = req.context['doc']
            # logger.debug('username:%s, password:%s, data:%s'
            #     % (username, password, post_data))
            # logger.debug('env:%s , \nstream:%s, \ncontext:, \ninput:' % (
            #     req.env, req.stream.read()))
        except Exception as ex:
            logger.error('error when try to get headers and data, ', ex)
            raise falcon.HTTPBadRequest('bad req',
                'when read from req, please check if the req is correct.')
        try:
            """
            handle_request:

            """
            status, objs_dict_list = obj.get_objs(patientid)

        except Exception as ex:
            logger.exception('error when get objs, ', ex)
            resp_dict['info'] = 'Error when get objs {}'.format(
                'obj')
            resp.status = falcon.HTTP_500
            resp.body = json.dumps(resp_dict, sort_keys=True, indent=4)
        else:
            if status:
                logger.debug('get objs ok, status positive')
                # resp_dict['info'] = 'Register {} success'.format(
                #     'obj')
                # resp_dict['objid'] = objid
                # resp.status = status or falcon.HTTP_200
                resp.status = falcon.HTTP_200
                resp.body = json.dumps(objs_dict_list)
            else:
                logger.exception('return error when try to get objs, ', ex)
                resp_dict['errinfo'] = 'Error when get objs {}'.format(
                    'obj')
                resp.status = falcon.HTTP_400
                resp.body = json.dumps(resp_dict)
                # resp.body = json.dumps(resp_dict, sort_keys=True,
                #     indent=4)


class AuthListener:

    def on_post(self, req, resp, role):
        """
        Get info of a patient in the system. The response data is in json format.

        :param req.header.username: username
        :param req.header.password: password
        :returns: a json contains doctor's info
                {"role":'d001', "info":{"info1":''}}
        """
        resp_dict = {}
        try:
            # username = req.get_header('username') or 'un'
            # password = req.get_header('password') or 'pw'
            # post_data = req.params.get('data')
            # have pre-processed by JSONTranslator, post_data is a dict
            post_data = req.context['doc']
            if not ('password' in post_data.keys() and 'username' in post_data.keys()):
                resp_dict['errinfo'] = 'Error, no password or username in post data'
                resp.status = falcon.HTTP_400
                resp.body = json.dumps(resp_dict)
            # logger.debug('username:%s, password:%s, data:%s'
            #     % (username, password, post_data))
            # logger.debug('env:%s , \nstream:%s, \ncontext:, \ninput:' % (
            #     req.env, req.stream.read()))
        except Exception as ex:
            logger.error('error when try to get headers and data, ', ex)
            raise falcon.HTTPBadRequest('bad req',
                'when read from req, please check if the req is correct.')
        try:
            """
            handle_request:

            """
            status, token_dict = auth.authentication(role, post_data)

        except Exception as ex:
            logger.exception('error when get objs, ', ex)
            resp_dict['info'] = 'Error when get objs {}'.format(
                'obj')
            resp.status = falcon.HTTP_500
            resp.body = json.dumps(resp_dict, sort_keys=True, indent=4)
        else:
            if status:
                logger.debug('get objs ok, status positive')
                # resp_dict['info'] = 'Register {} success'.format(
                #     'obj')
                # resp_dict['objid'] = objid
                # resp.status = status or falcon.HTTP_200
                resp.status = falcon.HTTP_201
                resp.body = json.dumps(token_dict)
            else:
                logger.exception('return error when try to get objs, ', ex)
                resp_dict['errinfo'] = 'Error when get objs {}'.format(
                    'obj')
                resp.status = falcon.HTTP_400
                resp.body = json.dumps(resp_dict)
                # resp.body = json.dumps(resp_dict, sort_keys=True,
                #     indent=4)
