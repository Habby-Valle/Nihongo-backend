import React from "react";
import { UseFormRegister } from "react-hook-form";
import { Column, Text } from "native-base";

interface ITextareaProps {
    label: string;
    name: string;
    register: UseFormRegister<any>;
}

export default function Textarea({ label, name, register }: ITextareaProps) {
    return (
        <Column space={2}>
            <Text
                fontSize="md"
                fontWeight="bold"
            >
                {label
            }</Text>
            <textarea
                className="textarea"
                placeholder={label.toLowerCase()}
                {...register(name, { required: true })}
                rows={5}

            />
        </Column>
    )
}