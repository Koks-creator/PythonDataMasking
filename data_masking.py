from typing import Union
import logging
from dataclasses import dataclass
import os
import PyPDF2
from fpdf import FPDF
from openai import OpenAI
from dotenv import load_dotenv
from email import policy
from email.parser import BytesParser
from email.generator import BytesGenerator

load_dotenv()


@dataclass
class CustomLogger:
    format: str = "%(asctime)s - %(name)s - %(levelname)s - Line: %(lineno)s - %(message)s"
    file_handler_format: logging.Formatter = logging.Formatter(format)
    log_file_name: str = "logs.log"
    logger_name: str = __name__
    logger_log_level: int = logging.ERROR
    file_handler_log_level: int = logging.ERROR

    def create_logger(self) -> logging.Logger:
        logging.basicConfig(format=self.format)
        logger = logging.getLogger(self.logger_name)
        logger.setLevel(self.logger_log_level)

        file_handler = logging.FileHandler(self.log_file_name)
        file_handler.setLevel(self.file_handler_log_level)
        file_handler.setFormatter(logging.Formatter(self.format))
        logger.addHandler(file_handler)

        return logger


logger = CustomLogger(
    logger_log_level=logging.DEBUG,
    file_handler_log_level=logging.DEBUG
).create_logger()


@dataclass
class OpenaiDataMasking:
    api_key: str
    start_msg: Union[str, os.PathLike]
    model: str = "gpt-4o-mini"

    def __post_init__(self) -> None:
        logger.info("Starting with parameters:\n"
                    f"{self.model=}\n"
                    f"{self.start_msg=}\n"
                    )
        self.openai = OpenAI(
            api_key=self.api_key
        )

        self.loaders = {
            "pdf": self.load_pdf_file,
            "eml": self.load_eml_file,
            "txt": self.load_text_file,
            "md": self.load_text_file,
        }

        self.savers = {
            "pdf": self.save_pdf,
            "eml": self.save_eml,
            "txt": self.save_text,
            "md": self.save_text,
        }

    def mask_data(self, content: str) -> str:
        chat_completion = self.openai.chat.completions.create(
            messages=[
                {"role": "system", "content": self.start_msg},
                {"role": "user", "content": content}
            ],
            model=self.model

        )
        assistant_response = chat_completion.choices[0].message.content
        return assistant_response

    @staticmethod
    def load_pdf_file(file_path: Union[str, os.PathLike]) -> str:
        with open(file_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            pdf_content = "\n".join([page.extract_text() for page in reader.pages])
            return pdf_content

    @staticmethod
    def load_eml_file(file_path: Union[str, os.PathLike]) -> str:
        with open(file_path, 'rb') as file:
            content = BytesParser(policy=policy.default).parse(file)
            return str(content)

    @staticmethod
    def load_text_file(file_path: Union[str, os.PathLike]) -> str:
        with open(file_path) as f:
            return f.read()

    @staticmethod
    def save_pdf(content: str, output_path: Union[str, os.PathLike]) -> Union[str, os.PathLike]:
        pdf = FPDF()

        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, content)
        pdf.output(output_path)

        return output_path

    @staticmethod
    def save_eml(content: str, output_path: Union[str, os.PathLike]) -> Union[str, os.PathLike]:
        content_bytes = content.encode('utf-8', errors='replace')

        mail_content = BytesParser(policy=policy.default).parsebytes(content_bytes)

        with open(output_path, "wb") as file:
            gen = BytesGenerator(file, policy=policy.default)
            gen.flatten(mail_content)

        return output_path

    @staticmethod
    def save_text(content: str, output_path: Union[str, os.PathLike]) -> Union[str, os.PathLike]:
        with open(output_path, "w") as f:
            f.write(content)
        return output_path

    def load_data(self, file_path: Union[str, os.PathLike]) -> str:
        _, extension = os.path.splitext(file_path)

        return self.loaders[extension.replace(".", "")](file_path=file_path)

    def save_data(self, content: str, output_path: Union[str, os.PathLike]) -> str:
        _, extension = os.path.splitext(output_path)

        return self.savers[extension.replace(".", "")](content=content, output_path=output_path)

    def mask_data_from_file(self, file_path: Union[str, os.PathLike], output_path: Union[str, os.PathLike]) -> str:
        logger.debug(f"Starting mask_data_from_file, loading content from: {file_path}")
        content = self.load_data(file_path=file_path)
        logger.debug("Content loaded")
        masked_data = self.mask_data(content=content)
        logger.debug("Data has been masked")
        self.save_data(content=masked_data, output_path=output_path)
        logger.debug(f"Data has been saved to: {output_path}")

        return masked_data


if __name__ == '__main__':
    API_KEY = os.environ["API_KEY"]
    with open("system_prompt.txt") as sp_f:
        START_MSG = sp_f.read()

    data_masking = OpenaiDataMasking(
        api_key=API_KEY,
        start_msg=START_MSG
    )
    data_masking.mask_data_from_file(file_path=f"Data/fake data.eml", output_path="Output/fake data_masked.eml")
