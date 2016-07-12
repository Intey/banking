import React, { Component }   from 'react'
import { bindActionCreators } from 'redux'
import { connect }            from 'react-redux'

import {
  TextField,
  DatePicker,
  AutoComplete,
  RaisedButton,
  CircularProgress
} from 'material-ui'

import * as eventActions from '../actions/EventPageAction.js'

export function EventPage(props) {
  // top:20px - fix position of progress bar.
  const ButtonOrProgress = (props.fetching ?
    <CircularProgress style={{top:"20px"}} size={0.5}/> :
    <RaisedButton label="Сохранить" primary={true}
      onClick={ props.eventActions.save }/>)
  const authorName = props.users[props.event.author].username
  // null_stub in DatePicker::onChange - is always undefined(no event).

  return(
    <div>
      <TextField floatingLabelText="Название" hintText="строка"
        onChange={(event) => props.eventActions.setName(event.target.value)}
        value={props.event.name}/>
      <TextField floatingLabelText="Цена" hintText="дробное число"
        onChange={(event) => props.eventActions.setPrice(event.target.value)}
        value={props.event.price}/>
      <DatePicker floatingLabelText="Дата события" hintText="нажмите для выбора"
        onChange={(null_stub, date) => props.eventActions.setDate(date)}
        value={props.event.date}/>
      <AutoComplete floatingLabelText="Автор" hintText="Выберите из списка"
          dataSource={props.users.map(u => u.username)}
          searchText={authorName}
          filter={(pattern, elem) => elem.startsWith(pattern)}
          onFocus={ e => e.target.select() }
          onNewRequest={ (text, index) => props.eventActions.setAuthor(index) }
          openOnFocus={true}/>
      <div className="row">
        { ButtonOrProgress }
      </div>
    </div>
  )
}

function mapStateProps(state) {
  return {
    // consts
    users: state.users,
    //payloads
    event: state.event,
    // requests
    fetching: state.fetching,
    error: state.error,
  }
}

function mapDispatchToProps(dispatch) {
  return {
    eventActions: bindActionCreators(eventActions, dispatch)
  }
}

export default connect(mapStateProps, mapDispatchToProps)(EventPage)