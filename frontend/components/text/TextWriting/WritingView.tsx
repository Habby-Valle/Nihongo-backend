import React, { useState } from "react"
import { Text, Column, Row, Button } from "native-base"
import { useTextWriting } from "../../../utils/api/text"
// @ts-ignore
import HTMLRenderer from 'react-html-renderer'
import Error from "../../Error"
import ModalDeleteTextWriting from "./ModalDeleteTextWriting"

interface IWritinglProps {
    textId: number
    onEdit: () => void
}

export default function WritingView(props: IWritinglProps) {

    const [modalDeleteText, setModalDeleteText] = useState<boolean>(false)

    const {
        data: text,
        error: textError,
        isLoading: textLoading,
    } = useTextWriting(props.textId)

    if (textError) {
        return <Error message={textError.message} />
    }

    if (textLoading) {
        return <Text>Loading...</Text>
    }

    return (
        <Column 
        width={'100%'}  
        px={3} 
        py={2}
        space={4}
    >
            <Column 
                space={4}
                _dark={{
                    bg: 'gray.700',
                }}
                _light={{
                    bg: 'white',
                }}
                p={"10px"}
                rounded={'md'}
                w={'45%'}
            >
                <HTMLRenderer html={text?.text} components={{ h1: Paragraph, p :Paragraph }} />
            </Column>
            <Row
                justifyContent={'space-around'}
                alignItems={'flex-start'}
                mt={'10px'}
            >
                <Column
                    space={4}
                    _dark={{
                        bg: 'gray.700',
                    }}
                    _light={{
                        bg: 'white',
                    }}
                    p={"10px"}
                    rounded={'md'}
                    w={'45%'}
                >   
                    <Text fontWeight={600} fontSize={15} textAlign={'center'}>Annotation</Text>
                    <HTMLRenderer  html={text?.annotation || '<p>Nenhuma anotação disponível</p>'}components={{ h1: Paragraph, p :Paragraph }} />
                    <Row
                        justifyContent={'space-around'}
                        alignItems={'flex-start'}
                        mt={'10px'}
                    >
                        <Button
                            bg={'#D02C23'}
                            _hover={{bg: '#ae251e'}}
                            _pressed={{bg: '#ae251e'}}
                            onPress={props.onEdit}
                        >
                            Edit text
                        </Button>
                        <Button
                            variant={'ghost'}
                            colorScheme={'red'}
                            onPress={() => setModalDeleteText(true)}
                        >
                            Delete text
                        </Button>
                    </Row>
                </Column>
            </Row>

            <ModalDeleteTextWriting
                isOpen={modalDeleteText}
                onClose={() => setModalDeleteText(false)}
                textId={props.textId}
            />
        </Column>
    )
}

function Paragraph(props: any) {
    return (
        <Text fontSize={16} fontWeight={500}>{props.children}</Text>
    )
}