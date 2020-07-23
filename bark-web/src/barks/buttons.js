import React  from 'react'

import {apiBarkAction} from './lookup'

export function ActionBtn(props) {
    const {bark, action, didPerformAction} = props
    const likes = bark.likes ? bark.likes : 0
    const className = props.className ? props.className : 'btn btn-primary btn-sm'
    const actionDisplay = action.display ? action.display : 'Action'
    const handleActionBackEndEvent = (response, status) => {
        console.log(response, status)
        if((status === 200 || status === 201) && didPerformAction) {
            didPerformAction(response, status)
        }
    }
    const handleClick = (event) => {
        event.preventDefault()
        apiBarkAction(bark.id, action.type, handleActionBackEndEvent)
    }
    const display = action.type === 'like' ? `${likes} ${actionDisplay}` : actionDisplay
    return <button className = {className} onClick = {handleClick}>{display}</button>
  }