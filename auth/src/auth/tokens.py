

class Token(object):
    def __init__(self, data, expires_in):
        self.data = data
        self.expires_in = expires_in


class B2CTokenBuilder(object):
    def __init__(self, account_id):
        self.account_id = account_id

    def issue_access_token(self):
        data = 'accesstoken:{}'.format(self.account_id)
        expires_in = 3600
        return Token(data, expires_in)

    def issue_refresh_token(self):
        data = 'refreshtoken:{}'.format(self.account_id)
        expires_in = None
        return Token(data, expires_in)