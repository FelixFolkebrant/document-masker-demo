import React, { useState, useMemo } from 'react';

interface HighlightTextProps {
    fullText: string;
    maskingStrings: string[];
    setTextToPreserve: React.Dispatch<React.SetStateAction<string[]>>;
}

// Utility to escape regex special characters
const escapeRegExp = (text: string): string => text.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

// Utility to highlight text based on a list of masking strings
const highlightText = (text: string, masks: string[]): JSX.Element[] => {
    if (!masks.length) return [<span key="0">{text}</span>];
    const regex = new RegExp(`(${masks.map(escapeRegExp).join('|')})`, 'gi');
    const parts = text.split(regex);

    return parts.map((part, index) => {
        const isHighlighted = masks.some(mask => new RegExp(`^${escapeRegExp(mask)}$`, 'i').test(part));
        return isHighlighted ?
            <span key={index} className="bg-yellow-200">{part}</span> :
            <span key={index}>{part}</span>;
    });
};

const HighlightText: React.FC<HighlightTextProps> = ({ fullText, maskingStrings, setTextToPreserve }) => {
    const handleButtonClick = () => {
        const selection = window.getSelection();
        if (selection && selection.rangeCount > 0 && selection.toString().trim() !== '') {
            setTextToPreserve(current => [...current, selection.toString()]);
            console.log('Selected text:', selection.toString());
        }
    };

    // Memoize highlighted text to prevent unnecessary re-renders
    const highlightedText = useMemo(() => highlightText(fullText, maskingStrings), [fullText, maskingStrings]);

    return (
        <div className='w-screen py-8 px-16'>
            <button onClick={handleButtonClick} className='px-4 py-2 bg-blue-500 text-white mb-8'>Keep selected text visable</button>
            <button onClick={() => setTextToPreserve([])} className='px-4 py-2 bg-red-500 text-white mb-8'>Clear</button>
            <div className='flex'>
                <div className='w-8/12' style={{ whiteSpace: 'pre-wrap' }}>{highlightedText}</div>
                {maskingStrings ?
                
                    <div className='w-4/12'>
                    <h2 className='text-2xl'>Text to keep visable</h2>
                    {maskingStrings.map((text, index) => {
                        return (
                            <div key={index} className='p-2 my-4 bg-blue-500 text-white'>
                                {text}
                            </div>
                        );
                    })
                    }
                    </div>
                    :
                    <></>
            }
            </div>
        </div>
    );
};

export default HighlightText;
