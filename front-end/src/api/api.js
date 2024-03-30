import axios from 'axios';
export const getAIMessage = async (userQuery) => {

  try {
    const response = await axios.post('http://localhost:5000/chatbot', {
      query: userQuery,
    });
    console.log(response.data)
    // Axios automatically parses the JSON response
    return response.data; // This contains the role and content from the backend
  } catch (error) {
    console.error('Error fetching the AI message: ', error);
    return { role: "assistant", content: "Sorry, there was an error processing your request." };
  }

  // const message = 
  //   {
  //     role: "assistant",
  //     content: "Connect your backend here...."
  //   }

  // return message;
};
