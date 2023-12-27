import useSWR from "swr"
import axios from "axios"
import { fetcchSimple } from "./user"

interface ITextList {
    id: number
    title: string
    text: string
    translate: string
    annotation: string
    created_at: string
    created_by: number
    updated_at: string
}

interface ITextCreate {
    title: string
    text: string
    translate: string
    annotation: string
}

interface ITextUpdate {
    id: number
    title?: string
    text?: string
    translate?: string
    annotation?: string
}

export function useTexts(){
    interface ITextResponse{
        results: ITextList[]
    }

    const {
        data,
        error,
        isLoading,
        isValidating,
        mutate
    } = useSWR<ITextResponse>(`/api/texts`, fetcchSimple)

    return {
        data,
        error,
        isLoading,
        isValidating,
        mutate
    }
}

export function useText(id: number){
    interface ITextResponse{
        results: ITextList
    }

    const {
        data,
        error,
        isLoading,
        isValidating,
        mutate
    } = useSWR<ITextResponse>(`/api/text/${id}`, fetcchSimple)

    return {
        data,
        error,
        isLoading,
        isValidating,
        mutate
    }
}

export async function createText({title, text, translate, annotation}: ITextCreate){
    interface ITextResponse{
        message: string
    }
    try {
        const res = await axios.post<ITextResponse>(`/api/text`, {title, text, translate, annotation})
        return res.data.message
    } catch (error: any) {
        throw new Error(error.message)
    }
}

export async function updateText(id: number, {title, text, translate, annotation}: ITextUpdate){
    interface ITextResponse{
        message: string
    }
    try {
        const res = await axios.put<ITextResponse>(`/api/text/${id}`, {title, text, translate, annotation})
        return res.data.message
    } catch (error: any) {
        throw new Error(error.message)
    }
}