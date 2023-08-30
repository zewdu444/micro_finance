import {deleteCookie} from 'cookies-next'
import { deAuthenticate, authenticate, restoreAuthState } from "./authSlice";


export const loginUser =(user) => async (dispatch) => {
  try {
    dispatch(authenticate(user))
  } catch (error) {
    console.log(error)
  }
}

export const logoutUser = () => async (dispatch) => {
  try {
    dispatch(deAuthenticate())
    deleteCookie("token")
  } catch (error) {
    console.log(error)
  }
}

export const checkLogin = (user) => async (dispatch) => {
  try {
    dispatch(restoreAuthState(user))
  } catch (error) {
    console.log(error)
  }
}

