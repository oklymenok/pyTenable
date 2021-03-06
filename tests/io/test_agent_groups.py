from .fixtures import *
from tenable.errors import *
import uuid, time

@pytest.fixture
def agentgroup(request, api):
    group = api.agent_groups.create(str(uuid.uuid4()))
    def teardown():
        try:
            api.agent_groups.delete(group['id'])
        except NotFoundError:
            pass
    request.addfinalizer(teardown)
    return group

def test_add_agent_to_group_group_id_typeerror(api):
    with pytest.raises(TypeError):
        api.agent_groups.add_agent('nope', 1)

def test_add_agent_to_group_agent_id_typeerror(api):
    with pytest.raises(TypeError):
        api.agent_groups.add_agent(1, 'nope')

def test_add_agent_to_group_scanner_id_typeerror(api):
    with pytest.raises(TypeError):
        api.agent_groups.add_agent(1, 1, scanner_id='nope')

def test_add_agent_to_group_notfounderror(api):
    with pytest.raises(NotFoundError):
        api.agent_groups.add_agent(1, 1)

def test_add_agent_to_group_standard_user_permissionerror(stdapi):
    with pytest.raises(PermissionError):
        stdapi.agent_groups.add_agent(1, 1)

def test_add_agent_to_group(api, agentgroup, agent):
    api.agent_groups.add_agent(agentgroup['id'], agent['id'])

def test_add_mult_agents_to_group(api, agentgroup):
    agents = api.agents.list()
    task = api.agent_groups.add_agent(agentgroup['id'],
        agents.next()['id'],
        agents.next()['id']
    )
    assert isinstance(task, dict)
    check(task, 'container_uuid', str)
    check(task, 'status', str)
    check(task, 'task_id', str)

def test_configure_group_id_typeerror(api):
    with pytest.raises(TypeError):
        api.agent_groups.configure('nope', 1)

def test_configure_name_typeerror(api):
    with pytest.raises(TypeError):
        api.agent_groups.configure(1, 1)

def test_configure_scanner_id_typeerror(api):
    with pytest.raises(TypeError):
        api.agent_groups.configure(1, 1, scanner_id='nope')

def test_configure_standard_user_permissionerror(stdapi, agentgroup):
    with pytest.raises(PermissionError):
        stdapi.agent_groups.configure(agentgroup['id'], str(uuid.uuid4()))

def test_configure_change_name(api, agentgroup):
    api.agent_groups.configure(agentgroup['id'], str(uuid.uuid4()))

def test_create_name_typeerror(api):
    with pytest.raises(TypeError):
        api.agent_groups.create(True)

def test_create_scanner_id_typeerror(api):
    with pytest.raises(TypeError):
        api.agent_groups.create(str(uuid.uuid4()), 'nope')

def test_create_standard_user_permissionerror(stdapi):
    with pytest.raises(PermissionError):
        stdapi.agent_groups.create(str(uuid.uuid4()))

def test_create_agent_group(api, agentgroup):
    assert isinstance(agentgroup, dict)
    check(agentgroup, 'creation_date', int)
    check(agentgroup, 'id', int)
    check(agentgroup, 'last_modification_date', int)
    check(agentgroup, 'name', str)
    check(agentgroup, 'owner', str)
    check(agentgroup, 'owner_id', int)
    check(agentgroup, 'owner_name', str)
    check(agentgroup, 'owner_uuid', 'uuid')
    check(agentgroup, 'shared', int)
    check(agentgroup, 'timestamp', int)
    check(agentgroup, 'user_permissions', int)
    check(agentgroup, 'uuid', 'uuid')

def test_delete_attributeerror(api):
    with pytest.raises(TypeError):
        api.agent_groups.delete()

def test_delete_group_id_typeerror(api):
    with pytest.raises(TypeError):
        api.agent_groups.delete('nope')

def test_delete_scanner_id_typerror(api):
    with pytest.raises(TypeError):
        api.agent_groups.delete(1, scanner_id='nope')

def test_delete_agent_group(api, agentgroup):
    api.agent_groups.delete(agentgroup['id'])
    with pytest.raises(NotFoundError):
        api.agent_groups.details(agentgroup['id'])

def test_delete_agent_from_group_group_id_typeerror(api):
    with pytest.raises(TypeError):
        api.agent_groups.delete_agent('nope', 1)

def test_delete_agent_from_group_agent_id_typeerror(api):
    with pytest.raises(TypeError):
        api.agent_groups.delete_agent(1, 'nope')

def test_delete_agent_from_group_scanner_id_typeerror(api):
    with pytest.raises(TypeError):
        api.agent_groups.delete_agent(1, 1, scanner_id='nope')

def test_delete_agent_from_group_notfounderror(api):
    with pytest.raises(NotFoundError):
        api.agent_groups.delete_agent(1, 1)

def test_delete_agent_from_group_standard_user_permissionerror(stdapi):
    with pytest.raises(PermissionError):
        stdapi.agent_groups.delete_agent(1, 1)

def test_delete_agent_from_group(api, agent, agentgroup):
    api.agent_groups.add_agent(agentgroup['id'], agent['id'])
    api.agent_groups.delete_agent(agentgroup['id'], agent['id'])

def test_delete_mult_agents_from_group(api, agentgroup):
    agents = api.agents.list()
    alist = [agents.next()['id'], agents.next()['id']]
    api.agent_groups.add_agent(agentgroup['id'], *alist)
    time.sleep(1)
    task = api.agent_groups.delete_agent(agentgroup['id'], *alist)
    assert isinstance(task, dict)
    check(task, 'container_uuid', str)
    check(task, 'status', str)
    check(task, 'task_id', str)

def test_details_group_id_typeerror(api):
    with pytest.raises(TypeError):
        api.agent_groups.details('nope')

def test_details_scanner_id_typeerror(api):
    with pytest.raises(TypeError):
        api.agent_groups.details(1, scanner_id='nope')

def test_details_nonexistant_group(api):
    with pytest.raises(NotFoundError):
        api.agent_groups.details(1)

def test_details_standard_user_permissionserror(stdapi, agentgroup):
    with pytest.raises(PermissionError):
        stdapi.agent_groups.details(agentgroup['id'])

def test_details_of_an_agent_group(api, agentgroup):
    group = api.agent_groups.details(agentgroup['id'])
    check(group, 'creation_date', int)
    check(group, 'id', int)
    check(group, 'last_modification_date', int)
    check(group, 'name', str)
    check(group, 'owner', str)
    check(group, 'owner_id', int)
    check(group, 'owner_name', str)
    check(group, 'owner_uuid', 'uuid')
    check(group, 'shared', int)
    check(group, 'timestamp', int)
    check(group, 'user_permissions', int)
    check(group, 'uuid', 'uuid')
    assert group['id'] == agentgroup['id']

def test_task_status_group_id_typerror(api):
    with pytest.raises(TypeError):
        api.agent_groups.task_status('no', 'nope')

def test_task_status_task_uuid_typeerror(api):
    with pytest.raises(TypeError):
        api.agent_groups.task_status(1, 1)

def test_task_status_task_uuid_unexpectedvalueerror(api):
    with pytest.raises(UnexpectedValueError):
        api.agent_groups.task_status(1, 'nope')

def test_task_status(api, agentgroup):
    agents = api.agents.list()
    t1 = api.agent_groups.add_agent(agentgroup['id'], 
        agents.next()['id'],
        agents.next()['id']
    )
    task = api.agent_groups.task_status(agentgroup['id'], t1['task_id'])
    assert isinstance(task, dict)
    check(task, 'container_uuid', str)
    check(task, 'last_update_time', int)
    check(task, 'start_time', int)
    check(task, 'status', str)
    check(task, 'task_id', str)