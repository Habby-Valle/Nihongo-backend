import React, { useState } from "react"
import { Column, Box, Text, FlatList, Pressable, Divider } from "native-base"
import { useTexts, ITextList } from "../../../utils/api/text"
import { ListRenderItemInfo } from "react-native"
import Error from "../../Error"
import DataEmpty from "../../DataEmpty"
import { useRouter } from "next/router"

export default function TranslateList() {

    const {
        data: texts,
        error: textsError,
        isLoading: textsLoading,
    } = useTexts()

    const router = useRouter()
    console.log(texts)

    function headers() {
        return (
            <Column width={'100%'}  px={3} py={2}>
                <Text fontWeight={600} fontSize={20} textAlign={'left'}>Texts</Text>
            </Column>
        )
    }

    function item({ item }: ListRenderItemInfo<ITextList>) {
        return (
            <Pressable 
                onPress={() => router.push(`/text/translate-text/${item.id}`)}
            >
                <Box width={'100%'} px={3} py={2} textDecoration={'underline'}>
                    <Text>{item.title}</Text>
                </Box>
            </Pressable>
        )
    }


    if (textsError) {
        return <Error message={textsError.message} />
    }

    if (textsLoading) {
        return <Text>Loading...</Text>
    }

    return (
        <Box
            w={'22%'}
            _dark={{
                bg: 'gray.700',
            }}
            _light={{
                bg: 'white',
            }}
            rounded={10}
        >
            <FlatList
                data={texts}
                renderItem={item}
                keyExtractor={item => item.id.toString()}
                ListHeaderComponent={headers}
                ListEmptyComponent={<DataEmpty message={'No texts found'} />}
                ItemSeparatorComponent={() => <Divider bg={'#D02C23'} />}
            />
        </Box>
    )
}