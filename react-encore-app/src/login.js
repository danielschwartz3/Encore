import React, { Component } from 'react';
import Video from 'twilio-video';
import axios from 'axios';
import { Button } from 'reactstrap';
import TextField from '@material-ui/core/TextField';

/* May be able to make this part of Performance.js
    I'm not entirely sure how to pass the user's handle across. */

export default class Login extends Component {
    constructor(props){
        super();
        this.state = {
            userName: "",
            password: "",
        }
        this.updateUserName = this.updateUserName.bind(this);
        this.updatePassword = this.updatePassword.bind(this);
    }

    updateUserName(e){
        this.setState({
            userName: e.target.value,
        })
    }
    
    updatePassword(e){
        this.setState({
            password: e.target.value,
        })
    }

    login(e){
        // will probably need to fix
        fetch('http://127.0.0.1:5000/', {
            method: 'POST',
            body: JSON.stringify({
                userName: this.state.userName,
                password: md5(this.state.password),
            })
        })
        this.setState({
            password: "",
        })
    }

    render(){
        return(
            <div>
                <TextField onChange={this.updateUserName}></TextField>
                <TextField onChange={this.updatePassword}></TextField>
                <Button onClick={this.login}>Log In</Button>
            </div>
        )
    }
}