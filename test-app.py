import user.auth as auth
import json


def test_getuser():
    response = auth.getuser()
    data = json.loads(response.get_data(as_text=True))
    assert data['result'] == 'nf'
