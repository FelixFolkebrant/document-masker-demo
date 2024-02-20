import Image from "next/image";
import UploadForm from "./components/UploadForm";

export default function Home() {
  return (
    <>
      <div className="w-full flex justify-center my-24">
        <UploadForm />
      </div>
    </>
  );
}
