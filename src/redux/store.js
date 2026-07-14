import { configureStore } from "@reduxjs/toolkit";
import interactionReducer from "./interaction";

const store = configureStore({
  reducer: {
    interaction: interactionReducer,
  },
});

export default store;