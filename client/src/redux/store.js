import { configureStore } from "@reduxjs/toolkit";
import themesSlice from "./features/themes/themesSlice";
import authSlice from "./features/auth/authSlice";
const store = configureStore({
  reducer:{
   themes :themesSlice,
   auth:authSlice
  },
 })

 export default store;
