function Quantify($http, config)
{
    this.createAccount = function (email, password) {
        var url = config.auth_base_url + "/accounts";

        var request = {
            client_secret: config.client_secret,
            email: email,
            password: password,
        };

        return $http({
            url: url,
            method: "POST",
            data: JSON.stringify(request),
            headers: {'Content-Type': 'application/json'},
        });
    };

    this.loginAccount = function (email, password) {
        var url = config.auth_base_url + "/tokens";

        var request = {
            grant_type: 'password',
            email: email,
            password: password,
        };

        return $http({
            url: url,
            method: "POST",
            data: JSON.stringify(request),
            headers: {'Content-Type': 'application/json'},
        });
    };

    return this;
}
