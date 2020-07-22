import React , {useEffect, useState} from 'react'

import {apiBarkCreate, apiBarkAction, apiBarkList} from './lookup'

export function BarksComponent(props) {
    const textAreaRef = React.createRef()
    const [newBarks, setNewBarks] = useState([])
    const handleBackEndUpdate = (response, status) => {
        let tempNewBarks = [...newBarks]
        if(status === 201) {
            setNewBarks(tempNewBarks)
            tempNewBarks.unshift(response)
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
    return <div className = {props.className}>
        <div className = 'col-12 mb-3'>
            <form onSubmit = {handleSubmit}>
                <textarea ref = {textAreaRef} required = {true} className = 'form-control' name = 'tweet'>

                </textarea>
                <button type = 'submit' className = 'btn btn-primary my-3'>Bark</button>
            </form>
        </div>
        <BarksList newBarks = {newBarks}/>
    </div>
    
}

export function BarksList(props) {
    const [barksInit, setBarksInit] = useState([])
    const [barks, setBarks] = useState([])
    const [barksDidSet, setBarksDidSet] = useState(false)
    useEffect(() => {
        const final = [...props.newBarks].concat(barksInit)
        if(final.length !== barks.length) {
            setBarks(final)
        }
    }, [props.newBarks, barks, barksInit])
    useEffect(() => {
        if(barksDidSet === false) {
            const handleBarkListLookup =  (response, status) => {
                if(status === 200) {
                    setBarksInit(response)
                    setBarksDidSet(true)
                } else {
                    alert("There was an error")
                }
            }
            apiBarkList(handleBarkListLookup)
        }
    }, [barksInit, barksDidSet, setBarksDidSet])

    const handleDidRebark = (newBark) => {
        const updateBarksInit = [...barksInit]
        updateBarksInit.unshift(newBark)
        setBarksInit(updateBarksInit)
        const updateFinalBarks = [...barks]
        updateFinalBarks.unshift(barks)
        setBarks(updateFinalBarks)
    }
    return barks.map((item, index)=>{
        return <Bark 
        bark = {item}
        didRebark = {handleDidRebark} 
        className = 'my-5 py-5 border bg-white text-dark' 
        key = {`${index}-{item.id}`}/>
    })
}

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

export function ParentBark(props) {
    const {bark} = props
    return bark.parent ? <div className = 'row'>
        <div className = 'col-11 mx-auto p-3 border rounded'>
            <p className = 'mb-0 text-muted small'>Rebark</p>
            <Bark hideActions className = {' '} bark = {bark.parent} />
        </div>
    </div> : null
}

export function Bark(props) {
    const {bark, didRebark, hideActions} = props
    const [actionBark, setActionBark] = useState(props.bark ? props.bark : null)
    const className = props.className ? props.className : 'col-10 mx-auto col-md-6'

    const handlePerformAction = (newActionBark, status) => {
        if(status === 200) {
            setActionBark(newActionBark)
        } else if (status === 201) {
            if(didRebark) {
                didRebark(newActionBark)
            }
        }
    }

    return <div className={className}>
        <div>
            <p>{bark.id} - {bark.content}</p>
            <ParentBark bark = {bark} />
        </div>
        {(actionBark && hideActions !== true) && <div className='btn btn-group'>
            <ActionBtn bark = {actionBark} didPerformAction = {handlePerformAction} action={{type: "like", display:"Likes"}}/>
            <ActionBtn bark = {actionBark} didPerformAction = {handlePerformAction} action={{type: "unlike", display:"Unlike"}}/>
            <ActionBtn bark = {actionBark} didPerformAction = {handlePerformAction} action={{type: "rebark", display:"Rebark"}}/>
        </div>}
    </div>
}