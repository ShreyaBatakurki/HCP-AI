import { createSlice } from "@reduxjs/toolkit";

const interactionSlice = createSlice({
  name: "interaction",
  initialState: {
    doctor: "",
    hospital: "",
    topic: "",
    aiResponse: "",
  },
  reducers: {
    setInteraction: (state, action) => {
      return { ...state, ...action.payload };
    },
  },
});

export const { setInteraction } = interactionSlice.actions;
export default interactionSlice.reducer;