<template>
	<view class="content">
		<image class="logo" src="/static/logo.png"></image>
		<view>
			<text class="title">{{title}}</text>
		</view>
		<view class="button" >
			<button class="btn" @click="jumpPage">个人中心</button>
			
		</view>
		<div id="app" >
			{{greeting}}
			<input v-model="greeting"/>
			<hr />
			<div v-if="isVisible" class="box"></div>
		</div>
	</view>
</template>

<script >

	export default {
		data() {
			return {
				title: '首页',
				greeting: 'jerry',
				isVisible: true
			}
		},
		onLoad() {

		},
		methods: {
			jumpPage(){
				uni.navigateTo({
					url: '/pages/login/index'
				})
			}

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
	.button {
		color: red;
		/* background-color: yellow; */
	}
	.btn {
		/* color: red; */
		/* background-color: red; */
		color: black;
		display: block;
		margin: 200rpx
	}
</style>
