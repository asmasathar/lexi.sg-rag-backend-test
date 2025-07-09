# lexi.sg-rag-backend-test

This is a Retrieval-Augmented Generation (RAG) based legal assistant that uses OpenRouter with DeepSeek to answer legal queries using strictly provided document context.

---

##  Quick Start

Try it out using this public URL: https://ecfe20a46f27.ngrok-free.app/docs

OR

### 1. **Fork and Clone the Repository**

git clone https://github.com/<your-username>/lexi.sg-rag-backend-test.git
cd lexi.sg-rag-backend-test
2. Create and Activate Virtual Environment
python -m venv venv
# For Windows:
venv\Scripts\activate

3. Install Dependencies
pip install -r requirements.txt

5. Run the Server
uvicorn app.main:app --reload
This will start the FastAPI backend at:
 http://127.0.0.1:8000

To interact with the API using Swagger UI, visit:
 http://127.0.0.1:8000/docs

 Sample Query
Send a POST request to /query with this JSON body:

{
  "query": "Is an insurance company liable to pay compensation if a transport vehicle involved in an accident was being used without a valid permit?"
}


 Sample Response
{
  "answer": "No, the insurance company is not liable to pay compensation if the transport vehicle lacked a valid permit at the time of the accident.\n\n- **Reason**: Use of a vehicle in a public place without a permit constitutes a \"fundamental statutory infraction\" under the Motor Vehicles Act, 1988. This breach is distinct from cases involving driver license violations (e.g., fake license, wrong vehicle class). The insurer is exempt from liability and entitled to recover any compensation paid from the owner and driver.\n  **Source**: Context document stating, *\"Use of vehicle in public place without permit is fundamental statutory infraction... Onus not to be casted on insurer - Insurer entitled to recover the compensation from the owner and the driver.\"*",
  "citations": [
    {
      "text": "- Respondents For the Appellants :- Abhishek Atrey, Advocate. For the Respondents :- Amit Kumar Singh, Advocate. Motor Vehicles Act, 1988 Sections 166, 66 and 149 Accident - No permit - Liability to pay compensation - Vehicle at time of accident did not have permit - Use of vehicle in public place without permit is fundamental statutory infraction...",
      "source": "Amrit Paul Singh v. TATA AIG (SC NO ROUTE Permit insurance Co. Recover from Owner).docx"
    },
    {
      "text": "Motor Vehicles Act, 1988, Sections 149 and 173 - Appeal - Insurance Company is liable to pay even if accident occurs outside India - Once insured, the vehicle is insured to cover all geographical areas, where the vehicle is authorised by authorities to travel...",
      "source": "Anil Kumar v. Roop Kumar Sharma (P&H Claim Payable even vehicle outside India).docx"
    },
    {
      "text": "The provisions of the Motor Vehicles Act permit that compensation paid under 'No fault liability' can be deducted from the final amount awarded by the Tribunal...",
      "source": "Darshan Vs State of Punjab (Tyre Burst Claim Payable).pdf"
    }
  ]
}
