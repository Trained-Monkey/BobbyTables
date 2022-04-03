import { createSlice, PayloadAction } from '@reduxjs/toolkit'
import type { RootState } from '../../app/store'

// Define a type for the slice state
interface Location {
    country: string | undefined,
    location: string,
    lat: number | undefined,
    lng: number | undefined
}

interface Report {
    event_date: string,
    locations: Location[],
    diseases: string[],
    syndromes: string[],
}

interface Article {
    url: string,
    date_of_publication: Date,
    headline: string,
    main_text: string,
    id: number,
    reports: Report[],
}

interface ArticlesState {
  articles: Article[]
}

// Define the initial state using that type
const initialState: ArticlesState = {
  articles: []
}

export const articlesSlice = createSlice({
  name: 'articles',
  // `createSlice` will infer the state type from the `initialState` argument
  initialState,
  reducers: {
    clearArticles: state => {
        state.articles = []
    },
    addArticle: (state, action: PayloadAction<Article>) => {
        state.articles.push(action.payload)
    },
    addBulkArticles: (state, action: PayloadAction<Article[]>) => {
        action.payload.forEach((article) => {
            state.articles.push(article)
        })
    },
  }
})

export const { clearArticles, addArticle, addBulkArticles } = articlesSlice.actions

export default articlesSlice.reducer