import { configureStore } from "@reduxjs/toolkit";
import themesSlice from "./features/themes/themesSlice";
const store = configureStore({
  reducer:{
   themes :themesSlice
  },
 })

 export default store;
