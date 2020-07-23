import React , {useState} from 'react'
import {ActionBtn} from './buttons'


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
    const path = window.location.pathname
    const match = path.match(/(?<barkid>\d+)/)
    const urlBarkId = match ? match.groups.barkid : -1
    const isDetail = `${bark.id}` === `${urlBarkId}`
    const handleLink = (event) => {
        event.preventDefault()
        window.location.href = `/${bark.id}`
    }
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
        <div className='btn btn-group'>
            {(actionBark && hideActions !== true) && <React.Fragment>
                <ActionBtn bark = {actionBark} didPerformAction = {handlePerformAction} action={{type: "like", display:"Likes"}}/>
                <ActionBtn bark = {actionBark} didPerformAction = {handlePerformAction} action={{type: "unlike", display:"Unlike"}}/>
                <ActionBtn bark = {actionBark} didPerformAction = {handlePerformAction} action={{type: "rebark", display:"Rebark"}}/>
            </React.Fragment>}
            {isDetail === true ? null : <button className = 'btn btn-sm btn-outline-primary' onClick = {handleLink}>View</button>}
        </div>
    </div>
}