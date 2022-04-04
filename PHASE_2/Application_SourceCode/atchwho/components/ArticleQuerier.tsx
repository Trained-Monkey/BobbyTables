import * as React from 'react';
import { useState, forwardRef } from 'react';

const axios = require('axios')

import CreatableSelect from 'react-select/creatable';
import makeAnimated from 'react-select/animated';
import { ActionMeta, OnChangeValue } from 'react-select'
import { Button } from 'react-bootstrap';


import {useDispatch} from 'react-redux'
import { useAppSelector, useAppDispatch } from '../app/hooks' 
import { addArticle, addBulkArticles, clearArticles } from '../features/article/articleSlice'

import {Selection} from './TimeQuerier'

import TimeQuerier from './TimeQuerier';


interface Location {
    locations: string[]
}

export default function ArticleQuerier(props: Location) {

    const dispatch = useAppDispatch()

    const defaultDateState:Selection = {
        startDate: new Date(),
        endDate: undefined,
        key: 'selection',
      }
    const defaultDatesState: Selection[] = [defaultDateState]
    const [dates, setDates] = useState(defaultDatesState);

    const defaultQueryState: string[] = []
    const [queries, setQueries] = useState(defaultQueryState)

    interface Option {
        readonly value: string,
        readonly label: string
    }

    const options: readonly Option[] = [
        {value: 'virus', label: 'Virus'},
        {value: 'outbreak', label: 'Outbreak'},
        {value: 'infection', label: 'Infection'},
        {value: 'fever', label: 'Fever'},
        {value: 'epidemic', label: 'Epidemic'},
        {value: 'infectious', label: 'Infectious'},
        {value: 'illness', label: 'Illness'},
        {value: 'bacteria', label: 'Bacteria'},
        {value: 'emerging', label: 'Emerging'},
    ]
    const animatedComponents = makeAnimated();

    function handleQueryChange(newValue: OnChangeValue<Option, true>, actionMeta: ActionMeta<Option>) {
        const results: string[] = []
        newValue.forEach((value:any) => {
            results.push(value.value)
        })
        setQueries(results)
    }

    function doRecursiveFetch(offset: number, limit: number = 20) {
        if (offset === 0) {
            dispatch(clearArticles())
        }
        console.log(props.locations)
        console.log(Array.isArray(props.locations))
        const params = {
            start_date: dates[0].startDate.toISOString().split('.')[0],
            end_date: dates[0].endDate?.toISOString().split('.')[0],
            key_terms: queries.join(','),
            location: props.locations.join(','),
            limit,
            offset
        }
        axios.get("https://seng3011-bobby-tables-backend.herokuapp.com/article", {params})
            .then((response: any) => {
                console.log(response)
                const data = response.data
                console.log(data)
                data.articles.forEach((articlePair: any) => {
                    const response_article = articlePair.article
                    const article = {
                        url: response_article.url,
                        date_of_publication: response_article.date_of_publication,
                        headline: response_article.headline,
                        main_text: response_article.main_text,
                        id: articlePair.articleId,
                        reports: response_article.reports,
                    }
                    dispatch(addArticle(article))
                })
                if (data.max_articles >= limit) {
                    doRecursiveFetch(limit, limit)
                }
            })
            .catch((error: any) => {
                console.error(error)
            })

    }

    return (
        <div style={{maxWidth: 575, backgroundColor: 'grey'}}>
            <TimeQuerier selections={dates} setSelections={setDates} />
            <div style={{display: 'flex', justifyContent: 'center'}}>
                <div style={{width: '100%'}}>
                    <CreatableSelect isMulti options={options} onChange={handleQueryChange} />
                </div>
                <div style={{width: '15%'}}>
                    <Button variant="primary" onClick={() => {doRecursiveFetch(0, 20)}}>Search</Button> 
                </div>
            </div>
        </div>
    )
};

