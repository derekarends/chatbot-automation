import React from "react";
import { PaperAirplaneIcon } from "@heroicons/react/24/outline";

type BaseProps = {
  value: string | number;
  onChange: (value: string | number) => void;
  debounce?: number;
};

type InputProps = BaseProps & {
  onKeyDown?: (e: React.KeyboardEvent<HTMLInputElement>) => void;
};

const DebouncedInput = ({
  value: initialValue,
  debounce = 500,
  onChange,
  onKeyDown,
  ...props
}: InputProps &
  Omit<React.InputHTMLAttributes<HTMLInputElement>, "onChange">) => {
  const [value, setValue] = React.useState(initialValue);

  React.useEffect(() => {
    setValue(initialValue);
  }, [initialValue]);

  React.useEffect(() => {
    const timeout = setTimeout(() => {
      onChange(value);
    }, debounce);

    return () => clearTimeout(timeout);
  }, [debounce, onChange, value]);

  return (
    <>
      <div className="relative w-full">
        <div className="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
          <PaperAirplaneIcon className="w-5 h-5 text-gray-900" />
        </div>
        <input
          type="text"
          className="w-full block p-1.5 pl-10 text-sm text-gray-900 border border-gray-300 rounded-lg bg-white focus:ring-1 focus:ring-purple-500 focus:border-purple-500"
          id="message-box"
          {...props}
          value={value}
          onChange={(e) => setValue(e.target.value)}
          onKeyDown={onKeyDown}
        />
      </div>
    </>
  );
};

type TextAreaProps = BaseProps & {
  onKeyDown?: (e: React.KeyboardEvent<HTMLTextAreaElement>) => void;
};

const DebouncedTextArea = ({
  value: initialValue,
  debounce = 500,
  onChange,
  onKeyDown,
  ...props
}: TextAreaProps &
  Omit<React.TextareaHTMLAttributes<HTMLTextAreaElement>, "onChange">) => {
  const [value, setValue] = React.useState(initialValue);

  React.useEffect(() => {
    setValue(initialValue);
  }, [initialValue]);

  React.useEffect(() => {
    const timeout = setTimeout(() => {
      onChange(value);
    }, debounce);

    return () => clearTimeout(timeout);
  }, [debounce, onChange, value]);

  return (
    <>
      <div className="relative w-full">
        <div className="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
          <PaperAirplaneIcon className="w-5 h-5 text-gray-900" />
        </div>
        <textarea
          rows={5}
          className="w-full block p-1.5 pl-10 text-sm text-gray-900 border border-gray-300 rounded-lg bg-white focus:ring-1 focus:ring-purple-500 focus:border-purple-500"
          id="message-box"
          {...props}
          value={value}
          onChange={(e) => setValue(e.target.value)}
          onKeyDown={onKeyDown}
        />
      </div>
    </>
  );
};

export { DebouncedInput, DebouncedTextArea };
