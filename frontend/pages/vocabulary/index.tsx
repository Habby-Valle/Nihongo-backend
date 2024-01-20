import React, {useState} from "react";
import { GetServerSidePropsContext } from "next";
import { redirectIfNoCredentials } from "../../utils";
import { BaseLayout } from "../../components/home/BaseLayout";
import WordList from "../../components/vocabulary/VocabularyList";
import SearchVocabulary from "../../components/vocabulary/SearchVocabulary";
import { Box } from "native-base";
import { IVocabularyFilters } from "../../components/vocabulary/SearchVocabulary";

export async function getServerSideProps({req, res}: GetServerSidePropsContext) {
    return redirectIfNoCredentials({req, res});
}


export default function Vocabulary() {
    const [filters, setFilters] = useState<IVocabularyFilters>()
    return (
        <BaseLayout title="Vocabulary">
            <Box
                justifyContent={'center'}
                alignItems={'center'}
                w={'100%'}
                flex={2}
            >
                <SearchVocabulary onFiltersChanged={setFilters}/>
                <WordList filters={filters} />    
            </Box>
        </BaseLayout>
            
    );
}