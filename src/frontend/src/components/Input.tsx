import React from "react";
import { PaperAirplaneIcon } from "@heroicons/react/24/outline";

type BaseProps = {
  value: string | number;
  onChange: (value: string | number) => void;
};

type InputProps = BaseProps & {
  onKeyDown?: (e: React.KeyboardEvent<HTMLInputElement>) => void;
};

const Input = ({
  value,
  onChange,
  onKeyDown,
  ...props
}: InputProps &
  Omit<React.InputHTMLAttributes<HTMLInputElement>, "onChange">) => {
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
          onChange={(e) => onChange(e.target.value)}
          onKeyDown={onKeyDown}
        />
      </div>
    </>
  );
};

export { Input };
