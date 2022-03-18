<template>
    <view class="login-wrapper">
        
		<!-- <view>
			<text class="title">{{title}}</text>
		</view> -->
        <view class="shading">
            <image class='logo' src="/static/images.jpeg" ></image>
        </view>

        <view class="whiteBg">
            <view class="list">
                <form @submit.prevent="submit">
                    <view class="item">
                        <view class="acea-row">
                            <image src="/static/images/phone_1.png" style="width: 24rpx; height: 34rpx;"></image>
                            <input class='input' type="text" ref="account" v-model="account" placeholder="输入手机号码" maxlength='11' required >
                        </view>
                    </view>

                    <view class="item">
                        <view class="acea-row">
                                <image src="/static/images/code_1.png" @click="changePwd" style="width: 28rpx; height: 32rpx;"></image>
                            <div v-if="pwdFlag">
                                <input class='input' type="text" ref="password" v-model="password" placeholder="填写登录密码" required >
                            </div>
                            <div v-else>
                                <input class='input' type="password" ref="password" v-model="password" placeholder="填写登录密码" required >
                            </div>
                        </view>
                    </view>

                </form>

            </view>


            <view class="logon" @click="submit">登录</view>
        </view>

    </view>


</template>

<script>
    import {login} from '@/apis/user'
	export default {
        name:'login',
		data() {
			return {
				title: '登录',
                account: '',
                password: '',
                pwdFlag:true
			}
		},
		onLoad() {

		},
		methods: {
            submit(){
                login({'account': this.account, 'password': this.password}).then(res => {
                    console.log(3424245)
                })
                .catch(res => {})
            },
            changePwd(){
                this.pwdFlag = !this.pwdFlag;
            }

            }

		}
	
</script>

<style >
    

.login-wrapper {
    padding: 30rpx;
    
}
.shading {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 100%;
        margin-top: 50rpx;
        /* margin-top: 200rpx; */
        

    }

.logo {
    height: 200rpx;
    width: 200rpx;
    margin: 200rpx auto 50rpx auto;
}
.whiteBg {
        margin-top: 100rpx;
        
    }

.list {
            border-radius: 16rpx;
            overflow: hidden;
            
        }

.item {
            border-bottom: 1px solid #f0f0f0;
            background: #fff;
        }

.acea-row {
    margin-left: 80rpx;
    display: inline-flex;
    justify-content: space-between;
    flex-direction: row;
    align-items: center;
    
}

.logon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 86rpx;
    margin-top: 80rpx;
    background-color: red;
    border-radius: 120rpx;
    color: white;
    font-size: 30rpx;
}

.input {
    margin-left: 40rpx;
}

    
</style>
