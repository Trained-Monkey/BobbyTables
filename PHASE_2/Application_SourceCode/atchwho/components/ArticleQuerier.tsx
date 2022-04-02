import * as React from 'react';
import { useState } from 'react';

const axios = require('axios')

import CreatableSelect from 'react-select/creatable';
import makeAnimated from 'react-select/animated';
import { ActionMeta, OnChangeValue } from 'react-select'


import {useDispatch} from 'react-redux'
import { useAppSelector, useAppDispatch } from '../app/hooks' 
import { addArticle, addBulkArticles, clearArticles } from '../features/article/articleSlice'

import {Selection} from './TimeQuerier'

import TimeQuerier from './TimeQuerier';


export default function ArticleQuerier() {

    const dispatch = useAppDispatch()

    let country: string = "Australia"

    const defaultDateState:Selection = {
        startDate: new Date(),
        endDate: undefined,
        key: 'selection',
      }
    const defaultDatesState: Selection[] = [defaultDateState]
    const [dates, setDates] = useState(defaultDatesState);

    const defaultQueryState: string[] = []
    const [queries, setQueries] = useState(defaultQueryState)

    const options = [
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

    function handleQueryChange(newValue: OnChangeValue<any, true>, actionMeta: ActionMeta<any>) {
        const results: string[] = []
        newValue.forEach((value) => {
            results.push(value.value)
        })
        setQueries(results)
    }

    function testFetch() {
        doRecursiveFetch('Malawi', 0)
    }

    function doRecursiveFetch(location: string, offset: number, limit: number = 20) {
        if (offset === 0) {
            dispatch(clearArticles())
        }
        const params = {
            start_date: dates[0].startDate.toISOString().split('.')[0],
            end_date: dates[0].endDate?.toISOString().split('.')[0],
            key_terms: queries.join(','),
            location,
            limit,
            offset
        }
        axios.get("https://seng3011-bobby-tables-backend.herokuapp.com/article", {params})
            .then((response: any) => {
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
                    doRecursiveFetch(location, limit, limit)
                }
            })
            .catch((error: any) => {
                console.error(error)
            })

    }


    return (
        <div style={{maxWidth: 740, backgroundColor: 'grey'}}>
            <TimeQuerier selections={dates} setSelections={setDates} />
            <div style={{maxWidth: '85%', margin: 20}}>
                <CreatableSelect isMulti options={options} components={animatedComponents} onChange={handleQueryChange} />
            </div>
            <button onClick={testFetch}>TEST</button>
        </div>
    )
}