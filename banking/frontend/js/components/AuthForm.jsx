import $ from 'jquery';
import React from 'react';

import {SubmitButton as Button} from './button.jsx'
import Edit from './edit.jsx';

import {AuthAPI} from '../domain/api.js'
import getToken from '../utils/token.js'

const API = new AuthAPI(getToken())

function onAuthenticated(response) {
    var token = response.token;
    window.localStorage.setItem('token', token);
    window.localStorage.setItem('user', JSON.stringify(response.account));
    document.location.href = (
        response.account.user.is_superuser ? '/admin/' : '/client/'
    );
}

export class AuthForm extends React.Component {
    constructor(props){
        super(props);
        this.state = {
            username: '',
            password: '',
            error: '',
        }

        this.handleUsernameChange = this.handleUsernameChange.bind(this);
        this.handlePasswordChange = this.handlePasswordChange.bind(this);
        this.handleAuth = this.handleAuth.bind(this);
        this.onError = this.onError.bind(this);
    }

    onError(error) {
        this.setState({error: error.responseJSON});
    }

    handleUsernameChange(event){
        this.setState({
            username: event.target.value
        });
    }

    handlePasswordChange(event){
        this.setState({
            password: event.target.value
        });
    }

    handleAuth(){
        var data = this.state;

        API.auth(this.state, onAuthenticated, this.onError);

    }

    render(){
        var has_error = !!this.state.error,
            error_component = has_error ?
            <div className="form-group">
                <div className="alert alert-danger">
                    {this.state.error}
                </div>
            </div> :
            null

        return (
            <form className="form-horizontal" name="auth-form" method="post">
                    <div className="form-group">
                        <legend>
                            <h3>Аутентификация</h3>
                        </legend>
                    </div>
                    {error_component}
                    <Edit Label="Username" Type="text" Error={has_error}
                        Change={this.handleUsernameChange}/>
                    <Edit Label="Password" Type="password" Error={has_error}
                        Change={this.handlePasswordChange}/>
                    <div className="form-group">
                        <Button Caption="Войти" Click={this.handleAuth} Form="auth-form"/>
                    </div>
            </form>
        );
    }
}