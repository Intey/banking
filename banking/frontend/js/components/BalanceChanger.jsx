import React from 'react'
import {AccountAPI} from '../domain/api.js';
import getToken from '../utils/token.js';

var API = new AccountAPI(getToken())

export default class BalanceChanger extends React.Component {
    constructor(props){
        super(props)
        this.state = {
            id: 1,
            count: 0,
            income: true
        }
        this.submit = this.submit.bind(this);
    }

    submit() {
        API.transfer(this.state,
                     response => console.log(response),
                     error => console.log(error)
                    );
    }
    render() { return (
        <div>
            <input value={this.state.count} type="number"/>
            <input type="checkbox" value={this.state.income}/>
            <button onClick={this.submit}>Выполнить</button>
        </div>
    )
    }
}
