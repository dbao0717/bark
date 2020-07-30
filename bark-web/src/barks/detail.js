import React , {useState} from 'react'
import {ActionBtn} from './buttons'

import {UserPicture, UserDisplay} from '../profiles'

export function ParentBark(props) {
    const {bark} = props
    return bark.parent ? <Bark isRebark rebarker={props.rebarker} hideActions className = {' '} bark = {bark.parent} /> : null
}

export function Bark(props) {
    const {bark, didRebark, hideActions, isRebark, rebarker} = props
    const [actionBark, setActionBark] = useState(props.bark ? props.bark : null)
    let className = props.className ? props.className : 'col-10 mx-auto col-md-6'
    className = isRebark === true ? `${className} p-2 border rounded` : className
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
        {isRebark === true && <div className='mb-2'> <span className='small text-muted'>Rebarked by <UserDisplay user={rebarker} /></span> </div>}
        <div className='d-flex'>
            <div className=''>
                <UserPicture user={bark.user} />
            </div>
            <div className= 'col-11'>
                <div>
                    <p>
                        <UserDisplay includeFullName user={bark.user} />
                    </p>
                    <p>{bark.content}</p>
                    <ParentBark bark = {bark} rebarker={bark.user} />
                </div>
                <div className='btn btn-group px-0'>
                    {(actionBark && hideActions !== true) && <React.Fragment>
                        <ActionBtn bark = {actionBark} didPerformAction = {handlePerformAction} action={{type: "like", display:"Likes"}}/>
                        <ActionBtn bark = {actionBark} didPerformAction = {handlePerformAction} action={{type: "unlike", display:"Unlike"}}/>
                        <ActionBtn bark = {actionBark} didPerformAction = {handlePerformAction} action={{type: "rebark", display:"Rebark"}}/>
                    </React.Fragment>}
                    {isDetail === true ? null : <button className = 'btn btn-sm btn-outline-primary' onClick = {handleLink}>View</button>}
                </div>
            </div>
        </div>
    </div>
}