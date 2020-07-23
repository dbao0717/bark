import React from 'react'
import {apiBarkCreate} from './lookup'

export function BarkCreate(props) {
    const textAreaRef = React.createRef()
    const {didBark} = props
    const handleBackEndUpdate = (response, status) => {
        if(status === 201) {
            didBark(response)
        } else {
            console.log(response)
            alert("An error has occurred. Please try again.")
        }
    }
    const handleSubmit = (event) => {
        event.preventDefault()
        const newVal = textAreaRef.current.value
        apiBarkCreate(newVal, handleBackEndUpdate)
        textAreaRef.current.value = ''
    }
    return <div className ={props.className}>
        <form onSubmit = {handleSubmit}>
            <textarea ref = {textAreaRef} required = {true} className = 'form-control' name = 'tweet'>

            </textarea>
            <button type = 'submit' className = 'btn btn-primary my-3'>Bark</button>
        </form>
    </div>
}