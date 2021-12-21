<template>
	<view class="content">
		<view>
			<text class="title">{{title}}</text>
		</view>
        <view class="phone-mask">
            <view class="input-item">
            
            <input type="text" v-model="account" placeholder="输入账号" maxlength='11' >
            </view>
            <view class="input-item">
                
            <input type="text" v-model="password" placeholder="输入密码" maxlength='11' >
            </view>
            <view class="sub_btn" @click="loginBtn">立即登录</view>
        </view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				title: '登录',
                account: '',
                password: '',
			}
		},
		onLoad() {

		},
		methods: {

		}
	}
</script>

<style>
	.content {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
	}

	.logo {
		height: 200rpx;
		width: 200rpx;
		margin: 200rpx auto 50rpx auto;
	}

	.text-area {
		display: flex;
		justify-content: center;
	}

	.title {
		font-size: 36rpx;
		color: #8f8f94;
	}
</style>
