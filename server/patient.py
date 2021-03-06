import json

from server.models import database, PatientModel, LoginModel
from server.hmsexceptions import UserNotExistException
from server.utils import logger


def register_patient(post_data):
    """
    Register a patient in the system. The post data is in json format.
    :param post_data: dict
    :returns: a status, a str( patient's info on success, err info on failure)
    """
    # print(post_data)
    patient = ''
    try:
        logger.debug('in register_patient')

        with database.atomic():
            patient = PatientModel.create_by_dict(post_data)
            logger.debug(patient)
            logger.debug('in database.atomic')
    # except peewee.IntegrityError:
    #     logger.warning('in patient model create except')

        # # `username` is a unique column, so this username already exists,
        # # making it safe to call .get().
        # old_user = AccountModel.get(AccountModel.username == username)
        # logger.warning('user exists...')
        # resp_dict['info'] = 'user exists, did not create user:%s' % username
        # resp.status = falcon.HTTP_409
        # try:
        #     change_user = AccountModel.get(AccountModel.username==username,
        #                     AccountModel.password==password)
        # except:
        #     logger.debug('change user data failed...')
    except Exception as ex:
        logger.error('Exception: ', ex)
        q = PatientModel.delete().where(PatientModel.email==patient)
        q.execute()
    try:
        with database.atomic():
            user = LoginModel.create_by_dict('patient', post_data)
            logger.debug(patient)
            logger.debug('in database.atomic')
    # except peewee.IntegrityError:
    #     logger.warning('in doctor model create except')

        # # `username` is a unique column, so this username already exists,
        # # making it safe to call .get().
        # old_user = AccountModel.get(AccountModel.username == username)
        # logger.warning('user exists...')
        # resp_dict['info'] = 'user exists, did not create user:%s' % username
        # resp.status = falcon.HTTP_409
        # try:
        #     change_user = AccountModel.get(AccountModel.username==username,
        #                     AccountModel.password==password)
        # except:
        #     logger.debug('change user data failed...')
    except Exception as ex:
        logger.error('Exception: ', ex)
        q = LoginModel.delete().where(LoginModel.username==patient)
        q.execute()
        return 0, 'create patient failed, did not create patient', ''
    else:
        return 1, str(patient), str(user.password)


def edit_patient(patientid, post_data):
    """
    Edit a patient in the system. The post data is a dict.

    :param post_data: dict
    :returns: a status, a str( patient's info on success, err info on failure)
    """
    # print(post_data)
    try:
        logger.debug('in edit_patient')
        PatientModel.update_by_dict(patientid, post_data)
        logger.debug('executed')
    # except peewee.IntegrityError:
    #     logger.warning('in doctor model create except')

        # # `username` is a unique column, so this username already exists,
        # # making it safe to call .get().
        # old_user = AccountModel.get(AccountModel.username == username)
        # logger.warning('user exists...')
        # resp_dict['info'] = 'user exists, did not create user:%s' % username
        # resp.status = falcon.HTTP_409
        # try:
        #     change_user = AccountModel.get(AccountModel.username==username,
        #                     AccountModel.password==password)
        # except:
        #     logger.debug('change user data failed...')
    except Exception as ex:
        logger.error('Exception: ', ex)
        return 0, 'edit_patient failed, did not edit_patient'
    else:
        return 1, str(patientid)


def get_patient(patientid):
    """
    Get info of a patient in the system.
    :param patientid: patient's uid
    :returns: a status, a str ( patient's info on success, err info on failure)
    """
    # print(patientid)
    info = {}
    try:
        logger.debug('in get_patient')
        patient_dict = PatientModel.get_dict(patientid)
        logger.debug(patient_dict)
    except UserNotExistException:
        logger.debug('in UserNotExistException')
        return 0, 'get patient failed, the required patient Did Not Exist'
    except Exception as ex:
        logger.error('Exception: ', ex)
        return 0, 'get patient failed'
    else:
        patient_json = json.dumps(patient_dict)
        logger.debug(patient_json)
        return 1, patient_json
