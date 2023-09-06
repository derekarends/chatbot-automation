import Avatar from "./Avatar";

type Props = {
  name: string;
  numberOfMessages: number;
};

function Header({ name, numberOfMessages = 0 }: Props) {
  return (
    <div className="border-b-2 border-b-gray-200 py-3 px-6 flex flex-row justify-between items-center">
      <div className="flex flex-row items-center space-x-1.5">
        <Avatar />
        <div className="flex flex-col items-start">
          <p className="text-xs text-gray-600">{name}</p>
          <p className="text-xs text-gray-400">{numberOfMessages} messages</p>
        </div>
      </div>
    </div>
  );
}

export default Header;
