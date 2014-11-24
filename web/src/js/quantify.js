function Quantify($http, config)
{
    this.createAccount = function(email, password) {
        var url = config.auth_base_url + "/accounts";

        var request = {
            client_secret: config.client_secret,
            email: email,
            password: password,
        };

        return $http({
            url: url,
            method: 'POST',
            data: JSON.stringify(request),
            headers: {'Content-Type': 'application/json'},
        });
    };

    this.loginAccount = function(email, password) {
        var url = config.auth_base_url + '/tokens';

        var request = {
            grant_type: 'password',
            email: email,
            password: password,
        };

        return $http({
            url: url,
            method: 'POST',
            data: JSON.stringify(request),
            headers: {'Content-Type': 'application/json'},
        });
    };

    this.getData = function(account_id, access_token) {
        var url = config.data_base_url + '/sensors/' + account_id;

        return $http({
            url: url,
            method: 'GET',
        });
    };

    this.getImportDataURL = function(account_id, access_token) {
        return config.data_base_url + '/sensors/' + account_id + '/file';
    };

    this.getExportDataURL = function(account_id, access_token) {
        return config.data_base_url + '/sensors/' + account_id + '/file';
    };

    this.deleteData = function(account_id, access_token) {
        var url = config.data_base_url + '/sensors/' + account_id;

        return $http({
            url: url,
            method: 'DELETE',
        });
    };

    return this;
}
