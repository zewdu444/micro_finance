import { createSlice } from '@reduxjs/toolkit';

const initialState = {
     mode: 'light'

}

export const themesSlice =createSlice({
  name:'themes',
  initialState,
  reducers :{
    setTheme :(state)=>{
       if(state.mode==='light'){
        return {
          ...state,
           mode:'dark'
        }
       }
       else{
        return {
          ...state,
           mode:'light'
        }
       }
    }
  }

})

export const {setTheme} =themesSlice.actions
export default themesSlice.reducer
