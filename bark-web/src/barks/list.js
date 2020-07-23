import React , {useEffect, useState} from 'react'
import {apiBarkList} from './lookup'
import {Bark} from './detail'

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
            apiBarkList(props.username, handleBarkListLookup)
        }
    }, [barksInit, barksDidSet, setBarksDidSet, props.username])

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