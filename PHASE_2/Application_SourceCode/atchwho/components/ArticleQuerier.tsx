import * as React from 'react';
import { useState } from 'react';

import CreatableSelect from 'react-select/creatable';
import makeAnimated from 'react-select/animated';
import { ActionMeta, OnChangeValue } from 'react-select'

import {Selection} from './TimeQuerier'

import TimeQuerier from './TimeQuerier';





export default function ArticleQuerier() {


    const defaultDateState:Selection = {
        startDate: new Date(),
        endDate: null,
        key: 'selection',
      }
    const [dates, setDates] = useState([
		defaultDateState
	  ]);

    const defaultQueryState: string[] = []
    const [queries, setQueries] = useState(defaultQueryState)

    const options = [
        {value: 'Virus', label: 'Virus'},
        {value: 'Outbreak', label: 'Outbreak'},
        {value: 'Infection', label: 'Infection'},
        {value: 'Fever', label: 'Fever'},
        {value: 'Epidemic', label: 'Epidemic'},
        {value: 'Infectious', label: 'Infectious'},
        {value: 'Illness', label: 'Illness'},
        {value: 'Bacteria', label: 'Bacteria'},
        {value: 'Emerging', label: 'Emerging'},
    ]
    const animatedComponents = makeAnimated();

    function handleQueryChange(newValue: OnChangeValue<any, true>, actionMeta: ActionMeta<any>) {
        const results: string[] = []
        newValue.forEach((value) => {
            results.push(value.label)
        })
        setQueries(results)
    }


    return (
        <div style={{maxWidth: 740, backgroundColor: 'grey'}}>
            <TimeQuerier selections={dates} setSelections={setDates} />
            <div style={{maxWidth: '85%', margin: 20}}>
                <CreatableSelect isMulti options={options} components={animatedComponents} onChange={handleQueryChange} />
            </div>
        </div>
    )
}