<script lang="ts">
  import { IC } from '$lib/icons';

  let showPassword = false;
</script>

<div class="login-wrapper">
  <div class="login-card">

    <!-- Logo / Branding -->
    <div class="login-brand">
      <div class="brand-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d={IC.cart} />
        </svg>
      </div>
      <h1 class="brand-name">QuetzalShop</h1>
      <p class="brand-sub">Sistema POS</p>
    </div>

    <!-- Formulario -->
    <form class="login-form">
      <div class="qz-field">
        <label class="qz-label" for="email">Correo electrónico</label>
        <div class="qz-input-wrap">
          <span class="qz-input-icon">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d={IC.mail} />
            </svg>
          </span>
          <input
            id="email"
            type="email"
            class="qz-input has-icon"
            placeholder="usuario@quetzalshop.com"
          />
        </div>
      </div>

      <div class="qz-field">
        <label class="qz-label" for="password">Contraseña</label>
        <div class="qz-input-wrap">
          <span class="qz-input-icon">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d={IC.lock} />
            </svg>
          </span>
          <input
            id="password"
            type={showPassword ? 'text' : 'password'}
            class="qz-input has-icon"
            placeholder="••••••••"
          />
          <button
            type="button"
            class="toggle-pw"
            on:click={() => showPassword = !showPassword}
          >
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d={showPassword ? IC.eyeOff : IC.eye} />
            </svg>
          </button>
        </div>
      </div>

      <button type="submit" class="btn btn-purple btn-lg full" style="margin-top: 8px;">
        Ingresar
      </button>
    </form>

  </div>
</div>

<style>
  .login-wrapper {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, var(--p-800) 0%, var(--p-600) 100%);
    padding: 20px;
  }

  .login-card {
    background: #fff;
    border-radius: 16px;
    padding: 40px 36px;
    width: 100%;
    max-width: 380px;
    box-shadow: 0 24px 64px rgba(0, 0, 0, 0.2);
  }

  .login-brand {
    text-align: center;
    margin-bottom: 32px;
  }

  .brand-icon {
    width: 52px;
    height: 52px;
    background: var(--p-600);
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 14px;
    color: #fff;
  }

  .brand-icon svg {
    width: 26px;
    height: 26px;
  }

  .brand-name {
    font-size: 22px;
    font-weight: 700;
    color: var(--g-900);
    margin: 0 0 4px;
    letter-spacing: -0.4px;
  }

  .brand-sub {
    font-size: 13px;
    color: var(--g-400);
    margin: 0;
  }

  .login-form {
    display: flex;
    flex-direction: column;
    gap: 16px;
  }

  .toggle-pw {
    position: absolute;
    right: 10px;
    top: 50%;
    transform: translateY(-50%);
    border: none;
    background: none;
    cursor: pointer;
    color: var(--g-400);
    display: flex;
    padding: 4px;
    border-radius: 4px;
    transition: color 0.15s;
  }

  .toggle-pw:hover {
    color: var(--g-700);
  }
</style>
